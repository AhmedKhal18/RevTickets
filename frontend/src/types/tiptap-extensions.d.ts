declare module '@tiptap/extension-link' {
  import { Extension } from '@tiptap/core';
  interface LinkOptions {
    openOnClick?: boolean;
    HTMLAttributes?: Record<string, any>;
  }
  const Link: Extension<LinkOptions>;
  export default Link;
}

