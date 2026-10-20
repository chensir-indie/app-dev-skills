# Repository introduction structure

The introduction borrows organizational patterns, not wording or branding, from these mature projects:

- [Vercel Skills](https://github.com/vercel-labs/skills): actionable install commands, skill selection and agent-specific setup.
- [Anthropic Skills](https://github.com/anthropics/skills): describe skills as reusable workflows and expose their directories clearly.
- [Playwright](https://github.com/microsoft/playwright): connect concrete capabilities to executable examples and validation.
- [mattpocock/skills at 5beb35b](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2): route by the user's current problem, read the actual skill before recommending it, load references conditionally, and define stage completion and artifact handoffs. See the [detailed comparison and implementation record](mattpocock-skills-comparison-2026-10-20.md).

Our application: a concise value statement, skill input/output comparison, concrete capabilities, actual exported example, quick start, realistic requests, environment requirements and honest limitations. No affiliation or endorsement is implied.

Root READMEs provide selection and direct execution-contract links. Standalone READMEs provide installation and first-use support. `SKILL.md` defines the agent's branch and execution contract; detailed schemas stay in local references. The [workflow guide](workflows.md) covers stage handoffs without making standalone skills depend on collection files.

The workflow SVG is original documentation artwork. The screenshot contact sheet is an existing, actual export of the original synthetic starter. Neither is presented as proof of image-to-HTML pixel identity.
