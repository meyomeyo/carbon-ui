import glob
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generalized replacements based on what's in the component docs
    replacements = {
        '<- Homeに戻る': '<span class="ja"><- Homeに戻る</span><span class="en"><- Go Home</span>',
        '<- 戻る': '<span class="ja"><- 戻る</span><span class="en"><- Back</span>',
        '📝 コード': '<span class="ja">📝 コード</span><span class="en">📝 Code</span>',
        '要素の表示・非表示を切り替えます。': '<span class="ja">要素の表示・非表示を切り替えます。</span><span class="en">Toggle visibility of elements.</span>',
        '複数要素(.class)の取得と状態(.state)の一括操作です。': '<span class="ja">複数要素(.class)の取得と状態(.state)の一括操作です。</span><span class="en">Select multiple elements and manipulate state.</span>',
        'CarbonUI標準のステータスカラーを適用します。': '<span class="ja">CarbonUI標準のステータスカラーを適用します。</span><span class="en">Apply standard CarbonUI status colors.</span>',
        '要素の属性操作です。': '<span class="ja">要素の属性操作です。</span><span class="en">Manipulate element attributes.</span>',
        'タッチやジェスチャー等に最適化されたイベント群です。': '<span class="ja">タッチやジェスチャー等に最適化されたイベント群です。</span><span class="en">Events optimized for touch and gestures.</span>',
        '要素の属性や入力値の変更を監視して関数を実行します。': '<span class="ja">要素の属性や入力値の変更を監視して関数を実行します。</span><span class="en">Execute a function by observing mutations or input values.</span>',
        'ここは fetch() によって <code>component/about.html</code> から動的に読み込まれたコンポーネントです。': '<span class="ja">ここは fetch() によって <code>component/about.html</code> から動的に読み込まれたコンポーネントです。</span><span class="en">This component was dynamically loaded via fetch from <code>component/about.html</code>.</span>',
        'キャッシュ機構を利用しているため、2回目以降の遷移は瞬間的に切り替わります。': '<span class="ja">キャッシュ機構を利用しているため、2回目以降の遷移は瞬間的に切り替わります。</span><span class="en">Due to the caching mechanism, subsequent transitions are instantaneous.</span>',
        '無効化する': '<span class="ja">無効化する</span><span class="en">Disable</span>',
        '対象のボタン': '<span class="ja">対象のボタン</span><span class="en">Target Button</span>',
        '有効化する': '<span class="ja">有効化する</span><span class="en">Enable</span>',
        'トグル切り替え': '<span class="ja">トグル切り替え</span><span class="en">Toggle</span>',
        'クリア (元の状態に戻す)': '<span class="ja">クリア (元の状態に戻す)</span><span class="en">Clear State</span>',
        'ここに入力してテスト...': 'Input here to test...',
        '触ってみて！<br>(Tap / Swipe / LongPress)': '<span class="ja">触ってみて！</span><span class="en">Touch me!</span><br>(Tap / Swipe / LongPress)'
    }

    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filepath in glob.glob('/home/meyo/ドキュメント/carbonui/docs/component/*.html'):
    if not filepath.endswith('home.html'):
        process_file(filepath)

