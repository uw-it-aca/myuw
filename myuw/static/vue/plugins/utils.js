export class VisibilityTracker {
  constructor(
    {ratioThreshold = 0.9, durationThreshold = 2} = {},
    onFlush = () => {}
  ) {
    this.components = {};
    this.groups = {};
    this.ratioThreshold = ratioThreshold;
    this.durationThreshold = durationThreshold;

    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') {
        this.stopAndFlush(onFlush);
      } else if (document.visibilityState === 'visible') {
        this.restart();
      }
    });
  }

  update(comp, entry) {
    let screenCoveredRatio = 0;
    if (entry.rootBounds && entry.rootBounds.height !== 0) {
      const rootArea = entry.rootBounds.height * entry.rootBounds.width;
      const cardArea = entry.boundingClientRect.height * entry.boundingClientRect.width;
      screenCoveredRatio = 1 - (rootArea - (cardArea * entry.intersectionRatio)) / rootArea;
    }

    // Update or add the component
    if (!this.components[comp.$myuw.uid]) {
      this.components[comp.$myuw.uid] = {}
    }
    const compData = this.components[comp.$myuw.uid];
    compData.component = comp;
    compData.intersectionRatio = entry.intersectionRatio;
    compData.screenCoveredRatio = screenCoveredRatio;
    compData.isVisible = this.isCompVisible(comp);
    
    const compRoot = comp.$myuw.compRoot;
    if (!compRoot) return;

    // Group the component
    if (!this.groups[compRoot.$myuw.uid]) {
      const components = this.components;
      this.groups[compRoot.$myuw.uid] = {
        tag: compRoot.$myuw.tag,
        components: [],
        get isVisible() {
          return this.components.some((uid) => components[uid].isVisible);
        },
      };
    }
    if (
      this.groups[compRoot.$myuw.uid].components.indexOf(comp.$myuw.uid) === -1
    ) {
      this.groups[compRoot.$myuw.uid].components.push(comp.$myuw.uid);
    }

    const timer = this.updateGroupTimer(compRoot);
    const duration = (Date.now() - timer) / 1000;
    
    return {
      report: (
        !this.groups[compRoot.$myuw.uid].isVisible &&
        timer &&
        duration >= this.durationThreshold
      ),
      tag: compRoot.$myuw.tag,
      duration: duration,
    };
  }

  isCompVisible(comp) {
    let onScreen = false;
    const componentData = this.components[comp.$myuw.uid];

    // Report if the component it is mostly visible
    if (componentData.intersectionRatio > this.ratioThreshold) {
      onScreen = true;
    }

    // Covers the most screen space
    onScreen = onScreen || (Object.values(this.components).every(
      (comp) => comp.screenCoveredRatio <= componentData.screenCoveredRatio,
    ) && componentData.screenCoveredRatio > 0.1);

    return onScreen;
  }

  updateGroupTimer(group) {
    const groupData = this.groups[group.$myuw.uid];

    let timer = null;
    if (groupData.isVisible) {
      if (!groupData.timer) {
        groupData.timer = Date.now();
      }
      timer = groupData.timer;
    } else {
      timer = groupData.timer;
      groupData.timer = null;
    }

    return timer;
  }

  stopAndFlush(callbackfn) {
    Object.values(this.groups)
      .filter((groupData) => groupData.isVisible)
      .forEach((groupData) => {
        const duration = (Date.now() - groupData.timer) / 1000;

        groupData.stopped = true;
        groupData.timer = null;

        callbackfn({
          report: duration >= this.durationThreshold,
          tag: groupData.tag,
          duration: duration,
        });
      });
  }

  restart() {
    Object.values(this.groups)
      .filter((groupData) => groupData.stopped)
      .forEach((groupData) => {
        groupData.stopped = false;
        groupData.timer = Date.now();
      });
  }
}