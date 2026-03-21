import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We will manually replace key parts for docs.html
    if 'docs.html' in filepath:
        # Add the language switcher button near the header if not present
        if 'class="lang-switch"' not in content:
            content = content.replace('<body>', '<body>\n    <button class="lang-switch" onclick="toggleLang()">🌐 EN / JA</button>')
        
        # Add the JS snippet before </body>
        js_snip = """<script>
        function toggleLang() {
            const html = document.documentElement;
            const newLang = html.lang === 'ja' ? 'en' : 'ja';
            html.lang = newLang;
            localStorage.setItem('carbon_lang', newLang);
        }
        const savedLang = localStorage.getItem('carbon_lang') || (navigator.language.startsWith('ja') ? 'ja' : 'en');
        document.documentElement.lang = savedLang;
        """
        if 'function toggleLang' not in content:
            content = content.replace('<script>', js_snip, 1)

        # Basic replacements
        replacements = [
            ('<a href="index.html">← 戻る</a>', '<a href="index.html" class="ja">← 戻る</a><a href="index.html" class="en">← Back</a>'),
            ('<p>CarbonUIはシンプルで軽量なJavaScript UIライブラリです。jQueryライクなメソッドチェーンを用いながら、モダンな状態管理やSPAルーティング、各種ジェスチャーをサポートします。</p>', 
             '<p class="ja">CarbonUIはシンプルで軽量なJavaScript UIライブラリです。jQueryライクなメソッドチェーンを用いながら、モダンな状態管理やSPAルーティング、各種ジェスチャーをサポートします。</p>\n        <p class="en">CarbonUI is a simple and lightweight JavaScript UI library. It supports modern state management, SPA routing, and various gestures while using a jQuery-like method chain.</p>'),
            ('API リファレンス目次', '<span class="ja">API リファレンス目次</span><span class="en">API Reference Index</span>'),
            ('1. Core (取得・ライフサイクル)', '<span class="ja">1. Core (取得・ライフサイクル)</span><span class="en">1. Core (Select / Lifecycle)</span>'),
            ('2. CarbonWidget (単一要素操作)', '<span class="ja">2. CarbonWidget (単一要素操作)</span><span class="en">2. CarbonWidget (Single Element)</span>'),
            ('3. CarbonEls (複数要素操作)', '<span class="ja">3. CarbonEls (複数要素操作)</span><span class="en">3. CarbonEls (Multiple Elements)</span>'),
            ('4. State (状態管理)', '<span class="ja">4. State (状態管理)</span><span class="en">4. State Management</span>'),
            ('5. Store (データ保存)', '<span class="ja">5. Store (データ保存)</span><span class="en">5. Store (Web Storage)</span>'),
            ('6. Router (SPA遷移)', '<span class="ja">6. Router (SPA遷移)</span><span class="en">6. Router (SPA)</span>'),
            ('1. Core API (要素取得・ライフサイクル)', '<span class="ja">1. Core API (要素取得・ライフサイクル)</span><span class="en">1. Core API (Select & Lifecycle)</span>'),
            ('<p><code>carbon.*</code> オブジェクトから呼び出せる基本メソッドです。</p>', '<p class="ja"><code>carbon.*</code> オブジェクトから呼び出せる基本メソッドです。</p><p class="en">Basic methods called from the <code>carbon.*</code> object.</p>'),
            ('<h4>要素の取得</h4>', '<h4 class="ja">要素の取得</h4><h4 class="en">Select Elements</h4>'),
            ('<tr><th>メソッド</th><th>戻り値</th><th>説明</th></tr>', '<tr><th>Method</th><th>Returns</th><th>Description</th></tr>'),
            ('指定したID(<code>#</code>不要)の要素を取得します。', '<span class="ja">指定したID(<code>#</code>不要)の要素を取得します。</span><span class="en">Get element by ID (no <code>#</code>).</span>'),
            ('指定したクラス(<code>.</code>不要)を持つ全ての要素を取得します。', '<span class="ja">指定したクラス(<code>.</code>不要)を持つ全ての要素を取得します。</span><span class="en">Get elements by class name (no <code>.</code>).</span>'),
            ('CSSセレクタで最初に一致する要素を取得します。', '<span class="ja">CSSセレクタで最初に一致する要素を取得します。</span><span class="en">Get the first element matching the CSS selector.</span>'),
            ('DOMの構築(DOMContentLoaded相当)が完了したタイミングでコールバックを実行します。既に完了している場合は即座に実行されます。', '<span class="ja">DOMの構築完了後に実行します。</span><span class="en">Execute callback after DOM is ready.</span>'),
            ('2. CarbonWidget (単一要素の操作)', '<span class="ja">2. CarbonWidget (単一要素の操作)</span><span class="en">2. CarbonWidget (Single Element)</span>'),
            ('で取得した要素は <code>CarbonWidget</code> としてラップされ、以下のメソッドをチェーンで利用できます。', 'で取得した要素はラップされ、チェーンで利用できます。</span><span class="en">Obtained elements are wrapped and can be method-chained.</span>'),
            ('<h4>プロパティ</h4>', '<h4 class="ja">プロパティ</h4><h4 class="en">Properties</h4>'),
            ('ラップされている元の生DOM要素', '<span class="ja">ラップされている元の生DOM要素</span><span class="en">The raw DOM element</span>'),
            ('状態管理(State)オブジェクトへのアクセス', '<span class="ja">状態管理(State)オブジェクト</span><span class="en">Access to State management</span>'),
            ('<h4>DOM操作・表示</h4>', '<h4 class="ja">DOM操作・表示</h4><h4 class="en">DOM & Visibility</h4>'),
            ('<tr><th>メソッド</th><th>説明</th></tr>', '<tr><th>Method</th><th>Description</th></tr>'),
            ('要素の <code>display: none</code> を解除し表示します。', '<span class="ja">要素を表示します。</span><span class="en">Show the element.</span>'),
            ('要素に <code>display: none</code> を設定して隠します。', '<span class="ja">要素を隠します。</span><span class="en">Hide the element.</span>'),
            ('表示/非表示を切り替えます。', '<span class="ja">表示/非表示を切り替えます。</span><span class="en">Toggle visibility.</span>'),
            ('要素が表示されているか (boolean) を返します。', '<span class="ja">表示状態を返します(boolean)。</span><span class="en">Returns true if visible.</span>'),
            ('要素が隠れているか (boolean) を返します。', '<span class="ja">非表示状態を返します(boolean)。</span><span class="en">Returns true if hidden.</span>'),
            ('要素のテキスト(textContent)を書き換えます。', '<span class="ja">テキストを設定します。</span><span class="en">Set textContent.</span>'),
            ('要素内のHTML(innerHTML)を書き換えます。', '<span class="ja">HTMLを設定します。</span><span class="en">Set innerHTML.</span>'),
            ('DOMから要素を完全に削除します。イベントも解除されます。', '<span class="ja">要素を完全に削除します。</span><span class="en">Remove element from DOM.</span>'),
            ('<h4>入力・フォーム補助</h4>', '<h4 class="ja">入力・フォーム</h4><h4 class="en">Forms & Inputs</h4>'),
            ('ボタン等に <code>disabled</code> 属性を付与します。', '<span class="ja">disabledを付与します。</span><span class="en">Add disabled attribute.</span>'),
            ('<code>disabled</code> 属性を解除します。', '<span class="ja">disabledを解除します。</span><span class="en">Remove disabled attribute.</span>'),
            ('input/textareaにおいて、入力値が空かどうか(boolean)を返します。', '<span class="ja">入力が空かどうか返します。</span><span class="en">Returns true if input is empty.</span>'),
            ('入力値が存在するか(boolean)を返します。', '<span class="ja">入力があるか返します。</span><span class="en">Returns true if input is filled.</span>'),
            ('<h4>イベントとジェスチャー</h4>', '<h4 class="ja">イベント・ジェスチャー</h4><h4 class="en">Events & Gestures</h4>'),
            ('クリックまたはタップ(touchstart)で発火します。引数: <code>(widget, event)</code>', '<span class="ja">タップ/クリックで発火。</span><span class="en">Triggers on click or tap.</span>'),
            ('フォーカス(focus)された際に発火します。', '<span class="ja">フォーカスで発火。</span><span class="en">Triggers on focus.</span>'),
            ('フォーカスが外れた(blur)際に発火します。', '<span class="ja">フォーカスが外れた際に発火。</span><span class="en">Triggers on blur.</span>'),
            ('長押しで発火します。第2引数で長押し判定のミリ秒(デフォルト500)を指定可能。', '<span class="ja">長押しで発火。</span><span class="en">Triggers on long press (ms).</span>'),
            ('スワイプした際、方向("up"|"down"|"left"|"right")を第2引数として返します。第2引数で判定距離(デフォルト50px)を指定可能。', '<span class="ja">スワイプで方向を返します。</span><span class="en">Returns swipe direction.</span>'),
            ('<h4>監視 (Observer)</h4>', '<h4 class="ja">監視 (Observer)</h4><h4 class="en">Observer</h4>'),
            ('要素の属性や値の変更をリアクティブに監視します。<br><code>prop === \'value\'</code> の場合はinputなどの入力変更を監視し、それ以外の場合は <code>data-*</code> などのDOM属性の変動を監視します。', '<span class="ja">属性や値の変更を監視します。</span><span class="en">Watch for attribute or value changes dynamically.</span>'),
            ('指定したpropの監視(MutationObserver/EventListener)を解除します。', '<span class="ja">監視を解除します。</span><span class="en">Stop watching the prop.</span>'),
            ('3. CarbonEls (複数要素の操作)', '<span class="ja">3. CarbonEls (複数要素の操作)</span><span class="en">3. CarbonEls (Multiple Elements)</span>'),
            ('で取得した要素リストを扱うラッパーです。取得した複数の要素に対して、自動的に一括処理を行います。', 'で取得した複数要素のラッパーです。</span><span class="en">Wrapper for a list of elements to process in bulk.</span>'),
            ('各要素(CarbonWidget)ごとにループ処理を実行します。コールバック引数: <code>(widget)</code>', '<span class="ja">各要素でループ処理。</span><span class="en">Loops over each widget.</span>'),
            ('リスト内の最初の要素を <code>CarbonWidget</code> として返します。', '<span class="ja">最初の要素を返します。</span><span class="en">Returns first widget.</span>'),
            ('取得できた要素の数を返します。', '<span class="ja">要素数を返します。</span><span class="en">Returns element count.</span>'),
            ('全要素に対してtappedイベントを一括でバインドします。', '<span class="ja">全てにtappedをバインド。</span><span class="en">Binds tapped to all.</span>'),
            ('全要素を一括で表示します。', '<span class="ja">全てを表示します。</span><span class="en">Show all elements.</span>'),
            ('全要素を一括で非表示にします。', '<span class="ja">全てを非表示にします。</span><span class="en">Hide all elements.</span>'),
            ('4. State (状態管理API)', '<span class="ja">4. State (状態管理API)</span><span class="en">4. State API</span>'),
            ('CarbonWidget の <code>.state</code> プロパティからアクセスする状態管理特化のAPIです。<br>状態を適用すると自動的に <code>carbon-[name]</code> クラスと <code>data-carbon-state="[name]"</code> 属性がDOMに付与され、スタイルの切り替えや状態把握がスムーズになります。', '<span class="ja">状態管理APIです。<code>carbon-[name]</code>が付与されます。</span><span class="en">State management API. Automatically applies <code>carbon-[name]</code> class.</span>'),
            ('指定した状態(CSSクラスとdata属性)を適用します。', '<span class="ja">状態を適用します。</span><span class="en">Applies state.</span>'),
            ('指定した状態を解除します。', '<span class="ja">状態を解除します。</span><span class="en">Removes state.</span>'),
            ('現在その状態が適用されているか (boolean) を返します。', '<span class="ja">適用中か返します。</span><span class="en">Returns true if state is applied.</span>'),
            ('現在適用されている状態名(data-carbon-state)を文字列で返します。', '<span class="ja">現在の状態名を返します。</span><span class="en">Returns current state name.</span>'),
            ('付与されているすべての <code>carbon-*</code> 状態を初期化（削除）します。', '<span class="ja">すべての状態をクリア。</span><span class="en">Clears all states.</span>'),
            ('5. Store (Web Storage 操作)', '<span class="ja">5. Store (Web Storage)</span><span class="en">5. Store (Web Storage)</span>'),
            ('<code>carbon.store</code> オブジェクト経由で sessionStorage への読み書きを安全に行います。<br>オブジェクトや配列は自動で JSON エンコード/デコードされ、キーの重複を防ぐため自動的に <code>carbon_</code> プレフィックスが付与されます。', '<span class="ja">sessionStorageへの安全なI/O。JSON結合やプレフィックス対応。</span><span class="en">Safe I/O for sessionStorage. Auto JSON encode/decode.</span>'),
            ('データを保存します。オブジェクトや配列もそのまま渡せます。', '<span class="ja">データを保存します。</span><span class="en">Save data.</span>'),
            ('keyに対応するデータを取得(デコード)して返します。無い場合は <code>undefined</code>。', '<span class="ja">データを取得します。</span><span class="en">Get data.</span>'),
            ('保存されたデータを削除します。', '<span class="ja">データを削除します。</span><span class="en">Delete data.</span>'),
            ('6. Router (SPAルーティング)', '<span class="ja">6. Router (SPA)</span><span class="en">6. Router (SPA)</span>'),
            ('Fetch APIとHistory APIを活用した超軽量ルーター機能です。ページをリロードせずにコンテンツを切り替え、キャッシュを活用してサクサク動作させます。', '<span class="ja">FetchとHistoryを用いた超軽量ルーター機能。</span><span class="en">Lightweight SPA router using Fetch and History APIs.</span>'),
            ('SPAルーターを初期化します。対象となるマウント領域(root)と初期ページ(home)を指定します。', '<span class="ja">ルーターを初期化します。</span><span class="en">Initialize SPA router.</span>'),
            ('指定したページ(<code>[pageName].html</code>) を非同期(fetch)で取得し、指定したroot要素内を書き換えます。<br>取得したHTMLはキャッシュされ、内部の <code>&lt;script&gt;</code> タグは自動的に再評価・実行されます。<br><code>replace = true</code> にするとブラウザに履歴(History)を追加せず上書き遷移します。', '<span class="ja">ページ遷移を非同期で実行します。</span><span class="en">Navigate asynchronously via fetch().</span>'),
            ('ブラウザの履歴(History API)を利用して前の状態(一つ前のページ)へ戻ります。', '<span class="ja">一つ前のページへ戻ります。</span><span class="en">Navigate back in history.</span>'),
            ('▶ プレイグラウンドで動作を確認する', '<span class="ja">▶ プレイグラウンドで動作を確認する</span><span class="en">▶ Try the Playground</span>')
        ]

        for old, new in replacements:
            content = content.replace(old, new)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

process_file('/home/meyo/ドキュメント/carbonui/docs/docs.html')

