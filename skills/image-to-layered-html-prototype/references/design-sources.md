# Design sources and optional tools

Checked: 2026-10-21. These links navigate sources and describe how this skill applies them; they are not installed packages, complete copies or guarantees of results. Read the relevant official sections when applying a rule and record the date. If inaccessible, mark it unverified rather than inventing a rule or claiming a tool was invoked.

## Optional skills

| Source | Method used here | Invocation boundary |
| --- | --- | --- |
| [Impeccable](https://github.com/pbakaus/impeccable) | Separate design judgment into focused critique, layout, typeset, polish and harden tasks; establish the product task before iterating | The upstream entry at the check date was `/impeccable <command> <target>`. Invoke only when actually available, after reading the installed version's instructions. The review workflow here runs independently; it does not require installing tools, initializing new project documents or executing every command |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Retrieve style, typography and stack guidance by context; combine a shared design system with explicit page variants | Use for undecided directions or missing standards. Search results are candidates, not authority over approved references. Reuse existing project tokens rather than maintaining a competing standard |
| [Vercel Web Design Guidelines](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md) / [rule source](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) | Check semantics, focus, content, interactions and resources before HTML delivery, locating issues in files/components | This concerns Web implementation quality, not aesthetic or pixel-fidelity proof. Apply individual recommendations in project context rather than treating it as a native-platform standard |

A skill name mentioned in conversation does not prove installation. Inspect the current available skills first. If any upstream tool is absent, continue the local [design quality review](design-quality-review.md); do not block reconstruction, install automatically or fabricate tool results. Prompt-only requests do not trigger HTML audits.

## Choose one primary design system

| Official source | When to consult | How to apply |
| --- | --- | --- |
| [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/) | Apple-platform interaction, layout, materials and accessibility | Read target-platform/control sections; preserve branding and the chosen design, distinguishing native constraints from visual revisions |
| [Material Design 3](https://m3.material.io/get-started) | Android or a product that explicitly chose Material | Extract adopted roles, states and variables from official component/style sections; using Flutter alone does not imply adopting all Material styling |
| [Carbon 2x Grid](https://www.carbondesignsystem.com/building-blocks/foundations/2x-grid/overview) | Grids, alignment and rhythm in dense content/business interfaces | Apply relevant layout principles without forcing a mobile consumer product into an enterprise style |
| [Ant Design](https://ant.design/docs/spec/introduce-cn/) | Organization and consistency in Chinese-language business interfaces | Read relevant patterns/states; supplement specific gaps in an existing primary system rather than mixing another skin |
| [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) | Testable Web accessibility requirements | Review applicable success criteria and levels; accessibility is a quality constraint, not a visual-style choice |
| [Refactoring UI](https://refactoringui.com/) | Learning specific interface adjustments and visual judgment | Optional learning source; cite accessible official public material, without requiring a purchase or copying/guessing paid chapters |

During the recorded check, HIG returned JavaScript/Markdown navigation and the Material entry returned a JavaScript placeholder. That did not verify all their content or specific dimensions. Obtain the actual relevant section when a task depends on a platform requirement. Other source checks also establish only inspected content, not a comprehensive audit.

Direct entries for common Web rules: [text contrast 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [text resizing 1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html), [reflow 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [target size 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html). Read exceptions and applicability; shorthand numbers are not unconditional gates for every page.

These methods were independently written around this skill's layered-reconstruction constraints. No upstream skill or paid book was copied, and no runtime dependency was added. If upstream code or text is introduced later, check the corresponding version's license and attribution requirements separately.
