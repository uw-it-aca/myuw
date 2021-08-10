<template>
  <div :id="id" class="modal fade">
    <div class="modal-dialog" :class="dialogClassCombined">
      <div class="modal-content">
        <div class="modal-header" :class="headerClass">
          <slot name="modal-title">
            <h5 class="modal-title" :class="titleClass"> {{ title }} </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            />
          </slot>
        </div>
        <div class="modal-body" :class="bodyClass">
          <slot />
        </div>
        <div class="modal-footer" :class="footerClass">
          <slot name="modal-footer" :hide="hide">
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';

export default {
  model: {
    prop: 'isOpen',
    event: 'toggled',
  },
  props: {
    id: {
      type: String,
      required: true,
    },
    isOpen: {
      type: Boolean,
      default: false,
    },
    size: {
      type: String,
      default: null,
    },
    dialogClass: {
      type: String,
      default: '',
    },
    title: {
      type: String,
      default: '',
    },
    titleClass: {
      type: String,
      default: '',
    },
    headerClass: {
      type: String,
      default: '',
    },
    bodyClass: {
      type: String,
      default: '',
    },
    footerClass: {
      type: String,
      default: '',
    },
    noCloseOnBackdrop: {
      type: Boolean,
      default: false,
    },
    noCloseOnEsc: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      modal: null,
      // Always synced with bootstrap. Is authoritative
      isOpenBT: false,
    };
  },
  computed: {
    dialogClassCombined() {
      let sizeClass = ' ';

      switch (this.size) {
        case 'sm':
          sizeClass += 'modal-sm';
          break;
        case 'lg':
          sizeClass += 'modal-lg';
          break;
        case 'xl':
          sizeClass += 'modal-xl';
          break;
      }

      return this.dialogClass + sizeClass;
    }
  },
  watch: {
    isOpen(newIsOpen) {
      console.log(newIsOpen, this.$el.classList.contains('show'))
      if (newIsOpen && !this.$el.classList.contains('show')) {
        this.modal.show();
      } else {
        this.modal.hide();
      }
      if (newIsOpen) {
        this.$emit('open');
        this.$emit('show');
      } else {
        this.$emit('close');
        this.$emit('hide');
      }
    },
    isOpenBT(newIsOpenBT, oldIsOpenBT) {
      if (newIsOpenBT == oldIsOpenBT) return;

      this.$emit('toggled', newIsOpenBT);
    }
  },
  mounted() {
    this.modal = Modal.getOrCreateInstance(
      this.$el,
      {
        backdrop: !this.noCloseOnBackdrop ? true : 'static',
        keyboard: !this.noCloseOnEsc,
      },
    );

    this.$el.addEventListener(
      'show.bs.modal',
      () => this.isOpenBT = true,
    );
    this.$el.addEventListener(
      'hide.bs.modal',
      () => this.isOpenBT = false,
    );
  },
  methods: {
    hide() {
      this.$emit('toggled', false);
    },
  }
};
</script>

<style lang="scss" scoped>
</style>