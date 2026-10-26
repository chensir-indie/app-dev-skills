# Collection scope

[Overview](README.md) · [Contributing](CONTRIBUTING.md) · [Workflow boundaries](docs/workflows.md)

## Responsibilities

App Dev Skills turns app evidence and design inputs into inspectable development artifacts. Its current responsibilities are:

| Responsibility | Output |
| --- | --- |
| Competitor analysis | Evidence-linked HTML and Design.md reports, UI/UX analysis, functional and technical maps, product implications |
| Design exploration and interface reconstruction | Concepts or prompts, editable layered pages, measured browser evidence |
| iOS resizability adaptation for SwiftUI, UIKit, Flutter, React Native, and WKWebView shells | Whole-app layout analysis, materialized official-rule ledgers, Apple HIG-linked recommendations, and a complete interactive HTML prototype with browser evidence |
| Store artwork | Editable localized covers, export matrices and review records |
| App publication orchestration | Project-owned Fastlane local build/signing, receipt-bound TestFlight upload, allowlisted metadata/screenshot delivery and separately authorized later store stages |

## Stage and adaptation boundaries

Skills may run independently or pass artifacts to another stage. Analysis, prototypes and artwork do not establish product implementation, device acceptance or store delivery. Each requested stage needs its own evidence.

iPhone Duo Adaptation defaults to whole-app layout analysis → recommendations → complete HTML prototype, with minimal changes to the original app design. An explicit audit/advice-only request narrows that endpoint; native implementation and device validation are separate. It is not Apple's official App Resizability Skill. Read the [adaptation workflow](docs/workflows.md#ios-framework-resizability-adaptation) for framework routing, workspace rules, builder handoff and device/browser evidence; the skill's own contracts govern execution.

## Adding a responsibility

Consider a new skill when a recurring app-development task has distinct inputs, actions and an observable result that cannot fit clearly into an existing skill. Explain the concrete problem, overlap, runtime cost, standalone installation and verification plan. A reproducible user need is more useful than an empty category or a generic list of agent advice.

Keep reusable contracts and portable checks here. Product-specific account mappings, private assets, credentials, release decisions and machine paths belong in the user's project. A user's explicit workflow takes precedence over repository defaults.

## Publication boundaries

App Publish Skill coordinates the existing project's release contract and actual platform/framework adapter. It keeps local artifacts, TestFlight upload receipts, listing delivery, tester acceptance, review and public availability distinct. A TestFlight upload stops at Apple's successful receipt; cover-only work belongs to App Store Cover Generator. Read the [publication workflow](docs/workflows.md#app-publication) for stage routing and authorization, and [runtime support](docs/runtime.md#publication-tools-and-project-runtimes) for project-toolchain checks. Installation and preflight grant no store authority.

## Infrastructure

Do not add a router, directory hierarchy, issue tracker, publishing integration or extra runtime solely to imitate another collection. Add infrastructure when the task requires it and its actual behavior can be verified. Revisit scope when the collection's responsibilities change; this document is not a ban on new skills.
