# Demo language coverage

The complete demo supplies explicit draft copy for every locale below: two stories, phone and tablet, 200 output cells. This covers the 50 presets in the [App Store catalog](../assets/locales/app-store.json), checked against [Apple’s localization list](https://developer.apple.com/help/app-store-connect/reference/app-information/app-store-localizations/) on 2026-10-12. It is not a claim to cover every language spoken in every country.

Run `npm run demo` to browse all locales. To keep an editable project, run `node scripts/init.mjs NEW_PROJECT --locales app-store`. For a subset, replace `app-store` with `ja,fr-CA,ur-PK`. The initializer without this option retains the small three-locale starter.

[Sample translations](../assets/locales/demo-copy.json) are authored drafts, not native-speaker-approved product copy. English regional versions and French regional versions intentionally share neutral demo wording in explicit records. Existing product expansion leaves new translations empty. Custom BCP 47 rendering locales remain supported through `locales.mjs add`; provide copy and suitable fonts for them.

| Locale | English name | Native name |
| --- | --- | --- |
| ar-SA | Arabic (Saudi Arabia) | العربية (المملكة العربية السعودية) |
| bn-BD | Bangla (Bangladesh) | বাংলা (বাংলাদেশ) |
| ca | Catalan | català |
| cs | Czech | čeština |
| da | Danish | dansk |
| de-DE | German (Germany) | Deutsch (Deutschland) |
| el | Greek | Ελληνικά |
| en-AU | Australian English | Australian English |
| en-CA | Canadian English | Canadian English |
| en-GB | British English | British English |
| en-US | American English | American English |
| es-ES | European Spanish | español de España |
| es-MX | Mexican Spanish | español de México |
| fi | Finnish | suomi |
| fr-CA | Canadian French | français canadien |
| fr-FR | French (France) | français (France) |
| gu-IN | Gujarati (India) | ગુજરાતી (ભારત) |
| he | Hebrew | עברית |
| hi | Hindi | हिन्दी |
| hr | Croatian | hrvatski |
| hu | Hungarian | magyar |
| id | Indonesian | Indonesia |
| it | Italian | italiano |
| ja | Japanese | 日本語 |
| kn-IN | Kannada (India) | ಕನ್ನಡ (ಭಾರತ) |
| ko | Korean | 한국어 |
| ml-IN | Malayalam (India) | മലയാളം (ഇന്ത്യ) |
| mr-IN | Marathi (India) | मराठी (भारत) |
| ms | Malay | Melayu |
| nl-NL | Dutch (Netherlands) | Nederlands (Nederland) |
| no | Norwegian | norsk |
| or-IN | Odia (India) | ଓଡ଼ିଆ (ଭାରତ) |
| pa-IN | Punjabi (India) | ਪੰਜਾਬੀ (ਭਾਰਤ) |
| pl | Polish | polski |
| pt-BR | Brazilian Portuguese | português (Brasil) |
| pt-PT | European Portuguese | português europeu |
| ro | Romanian | română |
| ru | Russian | русский |
| sk | Slovak | slovenčina |
| sl-SI | Slovenian (Slovenia) | slovenščina (Slovenija) |
| sv | Swedish | svenska |
| ta-IN | Tamil (India) | தமிழ் (இந்தியா) |
| te-IN | Telugu (India) | తెలుగు (భారతదేశం) |
| th | Thai | ไทย |
| tr | Turkish | Türkçe |
| uk | Ukrainian | українська |
| ur-PK | Urdu (Pakistan) | اردو (پاکستان) |
| vi | Vietnamese | Tiếng Việt |
| zh-Hans | Simplified Chinese | 简体中文 |
| zh-Hant | Traditional Chinese | 繁體中文 |
