# CarbonUI 🌑   

<img src="./logo.svg" width="200" />

> **「読んだらわかる」に特化した、jQueryライクなモダンUIライブラリ**

[🇬🇧 English](README.md)

CarbonUIは、独自記法でHTMLを汚さない、コードの意図がわかることをモットーにしたUIライブラリです。
jQueryライクなシンプルなメソッドチェーンを用いながら、モダンな状態管理、ジェスチャーイベント、簡易ルーティング(SPA)、データ保存などを標準でサポートしています。

## ✨ 特徴

- **直感的なDOM操作**: `carbon.id()`, `carbon.class()`, `carbon.find()` による要素取得とチェーン操作
- **強力な状態管理 (`State`)**: クラス(`carbon-*`)と`data-*`属性を用いた、シンプルで一貫性のある状態(State)切り替え
- **リッチなジェスチャーイベント**: `tapped`, `longPressed`, `swiped` など、スマートフォン対応イベントを標準搭載
- **SPAルーティング内蔵**: `fetch`ベースの軽量ルータキャッシュ。ページの切り替えと`<script>`の再評価を自動実行
- **リアクティブな変更監視 (`Watch`)**: `value`やカスタム属性の変更を`MutationObserver`で監視

---

## 🚀 はじめに

モジュールとして `carbon-ui.js` をインポートします。

```javascript
import carbon from 'https://cdn.jsdelivr.net/gh/meyomeyo/carbon-ui/carbon-ui.js';

carbon.ready(() => {
    // DOMツリーの構築完了後に実行されます
    carbon.id('my-button').tapped(() => {
        console.log('Button clicked or tapped!');
    });
});
```

*※注: DOM操作、イベント、状態管理、ストレージ機能を利用するだけであれば、`carbon.init()` を呼び出す必要はありません。`init()` はSPAルーティング機能を使用したい場合にのみ必要です。*

---

## 📖 ドキュメント ＆ デモ

CarbonUIのすべてのAPIリファレンスと、実際に動かして試せるプレイグラウンドは、以下の専用サイトをご覧ください。

👉 **[CarbonUI Official Documentation & Playground](https://meyomeyo.github.io/carbon-ui/)**

---

## 👤 Author
- **meyomeyo**

## 📄 License
MIT License © 2026 meyomeyo
