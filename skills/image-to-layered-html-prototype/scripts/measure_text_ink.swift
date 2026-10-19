// Read-only OCR aid for measuring visible glyph ink in a native-size screenshot.
// Usage: swift measure_text_ink.swift /absolute/path/to/image.png [language]
import Foundation
import Vision
import ImageIO
import CryptoKit

guard CommandLine.arguments.count >= 2 else {
    fputs("image path required\n", stderr)
    exit(2)
}
let url = URL(fileURLWithPath: CommandLine.arguments[1]).standardizedFileURL
guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
      let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
    fputs("cannot decode image\n", stderr)
    exit(2)
}
let data = try Data(contentsOf: url)
let digest = SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = [CommandLine.arguments.count > 2 ? CommandLine.arguments[2] : "zh-Hant", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(cgImage: image, options: [:]).perform([request])
let requestedTerms = CommandLine.arguments.count > 3 ? Array(CommandLine.arguments.dropFirst(3)) : []
let observations: [[String: Any]] = (request.results ?? []).compactMap { result in
    guard let candidate = result.topCandidates(1).first else { return nil }
    let box = result.boundingBox
    let substrings: [[String: Any]] = requestedTerms.compactMap { term in
        guard let range = candidate.string.range(of: term),
              let characters = try? candidate.boundingBox(for: range) else { return nil }
        let ink = characters.boundingBox
        return ["text": term, "bounds": [
            "x": Double(ink.minX) * Double(image.width),
            "y": Double(1 - ink.maxY) * Double(image.height),
            "width": Double(ink.width) * Double(image.width),
            "height": Double(ink.height) * Double(image.height),
        ]]
    }
    return [
        "text": candidate.string,
        "confidence": Double(candidate.confidence),
        "substrings": substrings,
        "bounds": [
            "x": Double(box.minX) * Double(image.width),
            "y": Double(1 - box.maxY) * Double(image.height),
            "width": Double(box.width) * Double(image.width),
            "height": Double(box.height) * Double(image.height),
        ],
    ]
}
let report: [String: Any] = [
    "schema": 1,
    "method": "Apple Vision VNRecognizeTextRequest accurate; source-image ink aid, not a CSS layout box",
    "image": url.path,
    "sha256": digest,
    "width": image.width,
    "height": image.height,
    "observations": observations,
]
let output = try JSONSerialization.data(withJSONObject: report, options: [.prettyPrinted, .sortedKeys])
FileHandle.standardOutput.write(output)
FileHandle.standardOutput.write(Data("\n".utf8))
