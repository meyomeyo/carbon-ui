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

## 📖 API Reference

### 🔍 Selecting Elements

Fetched elements are wrapped in either the `CarbonWidget` or `CarbonEls` class.

```javascript
const btn = carbon.id('submit-btn');     // Fetch by ID (CarbonWidget)
const items = carbon.class('list-item'); // Fetch multiple by class (CarbonEls)
const box = carbon.find('.container > .box'); // Fetch by CSS selector
```

### 👆 Events & Gestures

Easy-to-use event listeners which inherently support mobile devices.

```javascript
carbon.id('btn')
    .tapped((el, e) => console.log('Tapped!'))
    .longPressed((el) => console.log('Long pressed!'), 500)
    .swiped((el, dir) => console.log(`Swiped in direction: ${dir}`));
```

### 🎭 State Management (State)

Manage component states (e.g. `active`, `error`, `loading`). Applying a state adds a `carbon-[name]` class and a `data-carbon-state` attribute.

```javascript
const modal = carbon.id('my-modal');

modal.state.apply('active');   // <div class="carbon-active" data-carbon-state="active">
modal.state.is('active');      // true
modal.state.remove('active');
modal.state.clear();           // Clears all states
```

### 👁 Change Monitoring (Watch)

Observe changes to input values or DOM attributes.

```javascript
const input = carbon.id('username');

// Watch value changes
input.watch('value', (newVal) => {
    console.log('New input value:', newVal);
});

// Watch attribute changes
const icon = carbon.id('theme-icon');
icon.watch('data-theme', (newTheme, oldTheme) => {
    console.log(`Theme changed from ${oldTheme} to ${newTheme}`);
});

// Stop watching
input.unwatch('value');
```

### 🌐 Routing (SPA)

By simply calling `carbon.init()`, you can utilize hash-based simple SPA page transitions.
It asynchronously fetches `[pageName].html` and renders it into the target element.

```javascript
carbon.init({
    root: '#app',       // The target selector to render content
    home: 'component/home' // The initial file to load (component/home.html)
});

// Execute a page transition
carbon.go('component/about'); 

// Go back
carbon.back();
```

### 💾 Storage (Store)

Uses `sessionStorage` internally. It automatically encodes/decodes objects into JSON formats. A `carbon_` prefix is automatically added to the data keys.

```javascript
// Save data
carbon.store.set('userSettings', { theme: 'dark', fontSize: 14 });

// Retrieve data
const config = carbon.store.get('userSettings');

// Remove data
carbon.store.delete('userSettings');
```

### 🎨 Visibility & DOM Operations

```javascript
const panel = carbon.id('panel');

panel.show();
panel.hide();
panel.toggle();

if (panel.isVisible()) {
    panel.text('Currently visible!'); // Updates textContent
} else {
    panel.html('<strong>Hidden</strong>'); // Updates innerHTML
}

// Helpers for form validations
if (carbon.id('name-input').isEmpty()) {
    carbon.id('submit-btn').disable();
}
```

---

## 👤 Author
- **meyomeyo**

## 📄 License
MIT License © 2026 meyomeyo
