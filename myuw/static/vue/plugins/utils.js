export function findParentMyUWComponent(component) {
  let parentComponent = null;
  // Try to find the component tag
  for (let comp=component; comp && comp.$parent; comp = comp.$parent) {
    if (comp.$options._componentTag && comp.$options._componentTag.startsWith("myuw")) {
      parentComponent = comp;
      break;
    }
  }

  return parentComponent;
}

export function findParentMyUWComponentTag(component) {
  let parentComponent = findParentMyUWComponent(component);

  if (parentComponent) {
    return parentComponent.$options._componentTag.substr(5);
  }

  return null;
}