export const defaultTextFields = ["headline", "support", "uiTitle", "uiBody"];
export function textFields(project) {
  const fields = project.textFields ?? defaultTextFields;
  if (
    !Array.isArray(fields) ||
    !fields.includes("headline") ||
    new Set(fields).size !== fields.length ||
    fields.some((field) => !defaultTextFields.includes(field))
  )
    throw new Error(
      "textFields must be a unique subset of headline/support/uiTitle/uiBody including headline",
    );
  return fields;
}

export function auditedFields(project, slide) {
  return [
    ...textFields(project),
    ...((slide?.showBrand ?? project.showBrand ?? true) ? ["brand"] : []),
  ];
}
