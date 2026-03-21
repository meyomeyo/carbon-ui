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

## 📖 主なAPIリファレンス

### 🔍 要素の取得

取得した要素は `CarbonWidget` または `CarbonEls` クラスでラップされます。

```javascript
const btn = carbon.id('submit-btn');     // IDで取得 (CarbonWidget)
const items = carbon.class('list-item'); // クラスで複数取得 (CarbonEls)
const box = carbon.find('.container > .box'); // CSSセレクタで取得
```

### 👆 イベント・ジェスチャー

モバイル端末にも対応した使いやすいイベントリスナーが用意されています。

```javascript
carbon.id('btn')
    .tapped((el, e) => console.log('タップされました'))
    .longPressed((el) => console.log('長押しされました'), 500)
    .swiped((el, dir) => console.log(`${dir} 方向にスワイプされました`));
```

### 🎭 状態管理 (State)

コンポーネントの状態（`active`, `error`, `loading` など）を管理します。適用すると `carbon-[name]` クラスと `data-carbon-state` が付与されます。

```javascript
const modal = carbon.id('my-modal');

modal.state.apply('active');   // <div class="carbon-active" data-carbon-state="active">
modal.state.is('active');      // true
modal.state.remove('active');
modal.state.clear();           // 全ての状態をクリア
```

### 👁 変更の監視 (Watch)

入力値やDOM属性の変化を監視します。

```javascript
const input = carbon.id('username');

// 値の監視
input.watch('value', (newVal) => {
    console.log('新しい入力内容:', newVal);
});

// 属性の監視
const icon = carbon.id('theme-icon');
icon.watch('data-theme', (newTheme, oldTheme) => {
    console.log(`テーマが ${oldTheme} から ${newTheme} に変わりました`);
});

// 監視の解除
input.unwatch('value');
```

### 🌐 ルーティング (SPA)

`carbon.init()` を呼び出すだけで、ハッシュによる簡単なSPAによるページ遷移を利用できます。
`[pageName].html` を非同期で取得し、ターゲット領域に描画します。

```javascript
carbon.init({
    root: '#app',       // 描画先のセレクター
    home: 'component/home' // 初期表示するファイル（component/home.html）
});

// ページ遷移を実行する
carbon.go('component/about'); 

// 戻る
carbon.back();
```

### 💾 ストレージ (Store)

内部的に `sessionStorage` を使用し、オブジェクトなどもJSON形式で自動的にエンコード/デコードします。データのキーには自動的に `carbon_` プレフィックスが付与されます。

```javascript
// 保存
carbon.store.set('userSettings', { theme: 'dark', fontSize: 14 });

// 取得
const config = carbon.store.get('userSettings');

// 削除
carbon.store.delete('userSettings');
```

### 🎨 表示/非表示・DOM操作

```javascript
const panel = carbon.id('panel');

panel.show();
panel.hide();
panel.toggle();

if (panel.isVisible()) {
    panel.text('表示中です！'); // textContentの更新
} else {
    panel.html('<strong>隠れています</strong>'); // innerHTMLの更新
}

// フォームバリデーション等の補助
if (carbon.id('name-input').isEmpty()) {
    carbon.id('submit-btn').disable();
}
```

---

## 👤 Author
- **meyomeyo**

## 📄 License
MIT License © 2026 meyomeyo
