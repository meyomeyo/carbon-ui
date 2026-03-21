# CarbonUI 🌑

<img src="./logo.svg" width="200" />

> **A modern, jQuery-like UI library that reads like plain English.**

[🇯🇵 日本語版はこちら](README-ja.md)

CarbonUI is a UI library built on the principle of making code intent clear without polluting HTML with proprietary syntax. While utilizing simple jQuery-like method chaining, it natively supports modern state management, advanced gesture events, simple routing (SPA), and data storage.

## ✨ Features

- **Intuitive DOM Manipulation**: Fetch and chain operations easily using `carbon.id()`, `carbon.class()`, and `carbon.find()`.
- **Powerful State Management (`State`)**: Simple and consistent state switching using `carbon-[name]` classes and `data-*` attributes.
- **Rich Gesture Events**: Comes with built-in smartphone-friendly event listeners such as `tapped`, `longPressed`, and `swiped`.
- **Built-in SPA Routing**: Lightweight `fetch`-based router caching. Automatically handles page transitions and re-evaluates `<script>` tags.
- **Reactive Change Monitoring (`Watch`)**: Monitor changes to `value` or custom DOM attributes using `MutationObserver`.

---

## 🚀 Getting Started

Import `carbon-ui.js` as a module.

```javascript
import carbon from 'https://cdn.jsdelivr.net/gh/meyomeyo/carbon-ui/carbon-ui.js';

carbon.ready(() => {
    // Executed after the DOM tree is fully constructed
    carbon.id('my-button').tapped(() => {
        console.log('Button clicked or tapped!');
    });
});
```

*Note: You do not need to call `carbon.init()` to use DOM manipulation, events, state management, or storage. `init()` is only required if you want to use the SPA routing features.*

---

## 📖 Documentation & Demo

For the full API reference and an interactive playground where you can test CarbonUI in action, please visit our official documentation site:

👉 **[CarbonUI Official Documentation & Playground](https://meyomeyo.github.io/carbon-ui/)**

---

## 👤 Author
- **meyomeyo**

## 📄 License
MIT License © 2026 meyomeyo
