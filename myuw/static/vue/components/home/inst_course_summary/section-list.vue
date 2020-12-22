<template>
  <div>
    <uw-section
      v-for="section in sections"
      :key="section.id"
      :section="section"
      :mobile-only="mobileOnly"
    >
      <template v-if="getLinkedSections(section).length">
        <b-button v-if="!isOpen"
                  v-b-toggle="`linked-sections-${section.id}`"
                  variant="link"
                  size="sm"
                  :aria-label="`SHOW LINKED SECTIONS for ${section.id}`"
                  title="Expand to show linked sections"
        >
          Show Linked Sections of {{ section.curriculum_abbr }}
          {{ section.course_number }} {{ section.section_id }}
        </b-button>

        <b-button v-else
                  v-b-toggle="`linked-sections-${section.id}`"
                  variant="link"
                  size="sm"
                  :aria-label="`HIDE LINKED SECTIONS for ${section.id}`"
                  title="Collapse to show linked sections"
        >
          Hide Linked Sections of {{ section.curriculum_abbr }}
          {{ section.course_number }} {{ section.section_id }}
        </b-button>

        <b-collapse :id="`linked-sections-${section.id}`"
                    :aria-label="`LINKED SECTIONS FOR ${section.id}`"
        >
          <uw-linked-section
            v-for="(sec, j) in getLinkedSections(section)" :key="j"
            :section="sec"
            :mobile-only="mobileOnly"
          />
        </b-collapse>
      </template>
      <hr>
    </uw-section>
  </div>
</template>

<script>
import LinkedSection from '../../_common/course/inst/linked-section.vue';
import Section from './section.vue';

export default {
  components: {
    'uw-section': Section,
    'uw-linked-section': LinkedSection,
  },
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    sections: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      isOpen: false,
    };
  },
  methods: {
    getLinkedSections(pSection) {
      return this.sections.filter(
          (section) => (!section.is_primary_section &&
          section.primary_section_label === pSection.section_label),
      );
    },
  },
};
</script>
