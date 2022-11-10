<template>

<div>
    <div class="small text-center mt-1 mb-4">
      <div>
        <hr class="mx-auto mb-2 bg-secondary" style="max-width:500px;">
        <span class="me-2 fst-italic text-muted">{{ prompt }}</span>
        <a
          href=""
          role="button"
          class="text-nowrap"
          data-bs-toggle="modal"
          :data-bs-target="'#' + id"
          ><font-awesome-icon :icon="faCommentDots" /> Share your feedback</a>
      </div>
    </div>


    <!-- Modal -->
    <div
      :id="id"
      class="modal fade"
      tabindex="-1"
      :aria-labelledby="id + 'Label'"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header border-0">
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <iframe
              :src="'https://docs.google.com/forms/d/e/' + formId + '/viewform?embedded=true'"
              width="100%"
              height="750"
              frameborder="0"
              marginheight="0"
              marginwidth="0"
              >Loading…</iframe
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { faCommentDots } from "@fortawesome/free-regular-svg-icons";

export default {
  name: 'FeedbackModal',
  props: {
    id: {
      type: String,
      required: true,
    },
    prompt: {
      type: String,
      required: true,
    },
    formId: {
      type: String,
      required: true,
    },
  },
  data: function () {
    return {
      faCommentDots,
    };
  },
};
</script>
