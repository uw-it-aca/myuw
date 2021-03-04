<template>
  <uw-panel :loaded="true">
    <template #panel-body>
      <div v-if="!renderedFromParam">
        <b-row :no-gutters="$mq !== 'desktop'">
          <b-col md="8">
            <p class="myuw-text-lg">
              This toolkit is designed to help you make the most of your time at UW.
              The articles here address four interconnected dimensions of the Husky
              Experience: Know Yourself, Know the World, Make Your Way, and Weave it
              Together. Wherever you are in your university career, use this toolkit
              to challenge yourself, explore your options, and integrate all you are
              learning - your Husky Experience is more than a major!
            </p>
          </b-col>
          <b-col md="4" class="p-4 text-center">
            <img :src="`${staticUrl}/images/HX_dimensions-1.0x.png`"
                  :srcset="`${staticUrl}/images/HX_dimensions-1.0x.png 1x, ${
                    staticUrl
                  }/images/HX_dimensions-1.5x.png 1.5x, ${
                    staticUrl
                  }/images/HX_dimensions-2.0x.png 2x`"
                  alt="Husky Experience dimensions diagram"
                  class="img-fluid mx-auto"
            />
          </b-col>
        </b-row>

        <div v-if="isReady" class="d-flex flex-row flex-wrap card-cols">
          <uw-card v-for="(cd, i) in cardData" :key="i" loaded>
            <template #card-heading>
              <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
                {{cd.title}}
              </h3>
            </template>
            <template #card-body>
              <div class="myuw-text-md">
                <p>
                  {{cd.intro}}
                </p>

                <div v-html="data[cd.id]" />
              </div>
            </template>
          </uw-card>
        </div>

        <h3 class="h5">Why We Made This Toolkit</h3>
        <div class="myuw-text-md">
          <p>
            We are a team of UW staff members who care about your success.
            We want to help you create the kind of Husky Experience that will
            serve you best. To do this, we gathered and curated advice from
            students, faculty, and staff from across UW on how to make the
            most of your time here.
          </p>
          <p>
            The toolkit was curated by Michaelann Jundt of Undergraduate
            Academic Affairs, Janice Fournier and William Washington of UW
            Information Technology and Katy DeRosier from the Office of the
            Provost.
          </p>
        </div>

        <h3 class="h5">How it works</h3>
        <div class="myuw-text-md">
          <p>
            These articles are delivered here via MyUW so that all students
            have access to these ideas and resources. New articles are highlighted
            each week on the home page to provide timely advice, but read and
            explore them anytime.
          </p>
          <p>We plan to add new articles and resources each academic year.</p>
        </div>
      </div>
      <div v-else>
        <div v-if="isReady" v-html="data" class="myuw-text-md"/>
      </div>
    </template>
  </uw-panel>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
import Panel from '../_templates/panel.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-panel': Panel,
  },
  data: function() {
    const param = new URL(window.location.href).searchParams.get('article');

    return {
      urlExtra: param ? param : 'list/',
      renderedFromParam: !!param,
      cardData: [
        {
          id: 'know-yourself',
          title: 'Know Yourself',
          intro: 'Know what interests and engages you. Test ideas you have about yourself. Build a supportive social network and make decisions that are right for you. Understand how taking care of yourself is fundamental to success in everything you do.',
        },
        {
          id: 'know-world',
          title: 'Know the World',
          intro: 'What are you curious about? What matters to you? Know how the people and resources at the UW can help you learn, understand, and contribute.',
        },
        {
          id: 'make-your-way',
          title: 'Make Your Way',
          intro: 'Gather tools and knowledge to intentionally construct a career. Learn to identify and showcase your skills and strengths. Build a professional network to support you on a path to success.',
        },
        {
          id: 'weave-together',
          title: 'Weave it Together',
          intro: 'Reflect on your experiences large and small – how do they connect? Weave your experiences into a meaningful whole – the story of your growth and learning.',
        },
      ],
    };
  },
  computed: {
    ...mapState({
      hxtViewer: (state) => state.user.affiliations.hxt_viewer,
      staticUrl: (state) => state.staticUrl,
    }),
    ...mapState('hx_toolkit', {
      hxToolkit: (state) => state.value,
    }),
    ...mapGetters('hx_toolkit', [
      'isReadyTagged',
    ]),
    isReady() {
      return this.isReadyTagged(this.urlExtra);
    },
    data() {return this.hxToolkit[this.urlExtra];},
  },
  mounted() {
    if (this.hxtViewer) {
      this.fetch(this.urlExtra);
    }
  },
  methods: {
    ...mapActions('hx_toolkit', {
      fetch: 'fetch',
    }),
  },
}
</script>

<style lang="scss" scoped>
@use 'sass:map';
@use '../../../css/myuw/variables.scss' as b-vars;

::v-deep .myuw-article-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding-top: 1rem;
  margin-top: 2rem;
}

::v-deep .myuw-article-footer-title {
  font-family: 'Open Sans', sans-serif !important;
  font-weight: bold;
}

::v-deep h3 {
  font-size: 1.25rem;
}

div.d-flex.card-cols > div {
  display: flex;
}

@media (min-width: map.get(b-vars.$grid-breakpoints, md)) {
  $num-cols: 2;
  $middle-margin-size: 20px;
  div.d-flex.card-cols > div {
    width: calc((100% / #{$num-cols}) - (#{$middle-margin-size} / #{$num-cols}));
  }
  div.d-flex.card-cols > div:nth-child(odd) {
    margin-right: $middle-margin-size;
  }
}
@media (max-width: map.get(b-vars.$grid-breakpoints, md)) {
  div.d-flex.card-cols > div {
    width: 100%;
  }
}
</style>