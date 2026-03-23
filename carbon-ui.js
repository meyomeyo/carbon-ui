/**
 * CarbonUI - Fucking useful UI wrapper for Frontend development.
 * @author MEYO
 * @version 1.0.0
 */
class CarbonWidget {
    constructor(el) {
        this._el = el
        if (!el._carbon) {
            el._carbon = { watchers: {} }
        }
    }

    get raw() {
        return this._el
    }

    get state() {
        const el = this._el
        return {
            apply(name) {
                el.classList.add(`carbon-${name}`)
                el.dataset.carbonState = name
                return this
            },

            remove(name) {
                el.classList.remove(`carbon-${name}`)
                if (el.dataset.carbonState === name) {
                    delete el.dataset.carbonState
                }
                return this
            },

            is(name) {
                return el.classList.contains(`carbon-${name}`)
            },

            clear() {
                const toRemove = [...el.classList].filter(c => c.startsWith('carbon-'))
                toRemove.forEach(c => el.classList.remove(c))
                delete el.dataset.carbonState
                return this
            },

            current() {
                return el.dataset.carbonState || null
            }
        }
    }

    disable() {
        this._el.setAttribute('disabled', '')
        return this
    }

    enable() {
        this._el.removeAttribute('disabled')
        return this
    }

    tapped(fn) {
        let lastTouch = 0
        this._el.addEventListener('touchend', e => {
           e.preventDefault()
            lastTouch = Date.now()
            fn(this, e)
        }, { passive: false })
        this._el.addEventListener('click', e => {
            if (Date.now() - lastTouch < 500) return  // touchendの直後のclickを無視
            fn(this, e)
        })
        return this
    }

    focused(fn) {
        this._el.addEventListener('focus', e => fn(this, e))
        return this
    }

    unfocused(fn) {
        this._el.addEventListener('blur', e => fn(this, e))
        return this
    }

    longPressed(fn, ms = 500) {
        let timer = null
        this._el.addEventListener('touchstart', () => {
            timer = setTimeout(() => fn(this), ms)
        }, { passive: true })
        this._el.addEventListener('touchend', () => clearTimeout(timer))
        this._el.addEventListener('touchmove', () => clearTimeout(timer))
        this._el.addEventListener('mousedown', () => {
            timer = setTimeout(() => fn(this), ms)
        })
        this._el.addEventListener('mouseup', () => clearTimeout(timer))
        this._el.addEventListener('mouseleave', () => clearTimeout(timer))
        return this
    }

    swiped(fn, threshold = 50) {
        let startX, startY, startRect
        const getTouchPoint = (touch, rect) => {
            return {
                x: touch.clientX - rect.left,
                y: touch.clientY - rect.top
            }
        }
        this._el.addEventListener('touchstart', e => {
            startRect = this._el.getBoundingClientRect()
            const point = getTouchPoint(e.touches[0], startRect)
            startX = point.x
            startY = point.y
        }, { passive: true })
        this._el.addEventListener('touchend', e => {
            if (startX === undefined || startY === undefined || !startRect) return
            const point = getTouchPoint(e.changedTouches[0], startRect)
            const dx = point.x - startX
            const dy = point.y - startY
            if (Math.abs(dx) < threshold && Math.abs(dy) < threshold) return
            const dir = Math.abs(dx) > Math.abs(dy)
                ? (dx > 0 ? 'right' : 'left')
                : (dy > 0 ? 'down' : 'up')
            fn(this, dir)
            startX = undefined
            startY = undefined
            startRect = undefined
        }, { passive: true })
        return this
    }

    isEmpty() {
        const v = this._el.value ?? this._el.textContent
        return v.trim() === ''
    }

    isFilled() {
        return !this.isEmpty()
    }

    show() {
        this._el.style.display = ''
        this._el.removeAttribute('hidden')
        return this
    }

    hide() {
        this._el.style.display = 'none'
        return this
    }

    isVisible() {
        return this._el.style.display !== 'none' && !this._el.hidden
    }

    isHidden() {
        return !this.isVisible()
    }

    toggle() {
        if (this.isVisible()) {
            this.hide()
        } else {
            this.show()
        }
        return this
    }

    watch(prop, fn) {
        const el = this._el
        let watcher

        if (prop === 'value') {
            const handler = () => fn(el.value)
            el.addEventListener('input', handler)
            watcher = { disconnect: () => el.removeEventListener('input', handler) }
        } else {
            const observer = new MutationObserver(mutations => {
                mutations.forEach(m => {
                    if (m.attributeName === prop) {
                        fn(el.getAttribute(prop), m.oldValue)
                    }
                })
            })
            observer.observe(el, { attributes: true, attributeOldValue: true })
            watcher = observer
        }

        el._carbon.watchers[prop] = watcher
        return this
    }

    unwatch(prop) {
        const watcher = this._el._carbon.watchers[prop]
        if (watcher) {
            watcher.disconnect()
            delete this._el._carbon.watchers[prop]
        }
        return this
    }

    destroy() {
        Object.values(this._el._carbon.watchers).forEach(w => w.disconnect())
        this._el._carbon.watchers = {}
        return this
    }

    text(val) {
        if (val === undefined) return this._el.textContent
        this._el.textContent = val
        return this
    }

    html(val) {
        if (val === undefined) return this._el.innerHTML
        this._el.innerHTML = val
        return this
    }
}

class CarbonEls {
    constructor(els) {
        this._items = [...els].map(el => new CarbonWidget(el))
    }

    each(fn) {
        this._items.forEach(fn)
        return this
    }

    first() {
        return this._items[0] ?? null
    }

    count() {
        return this._items.length
    }

    tapped(fn) { this._items.forEach(w => w.tapped(fn)); return this }
    show() { this._items.forEach(w => w.show()); return this }
    hide() { this._items.forEach(w => w.hide()); return this }
}

const carbon = {
    store: {
        _prefix: 'carbon_',
        set(key, val) {
            try {
                sessionStorage.setItem(this._prefix + key, JSON.stringify(val))
            } catch (e) {
                console.warn(`[CarbonUI] store.set("${key}") failed`, e)
            }
            return this
        },
        get(key) {
            try {
                const raw = sessionStorage.getItem(this._prefix + key)
                return raw !== null ? JSON.parse(raw) : undefined
            } catch (e) {
                return undefined
            }
        },
        delete(key) {
            sessionStorage.removeItem(this._prefix + key)
            return this
        }
    },

    id(id) {
        const el = document.getElementById(id)
        if (!el) {
            console.warn(`[CarbonUI] #${id} が見つかりません`)
            return null
        }
        return new CarbonWidget(el)
    },

    class(className) {
        const els = document.querySelectorAll(`.${className}`)
        return new CarbonEls(els)
    },

    find(selector) {
        const el = document.querySelector(selector)
        if (!el) {
            console.warn(`[CarbonUI] "${selector}" が見つかりません`)
            return null
        }
        return new CarbonWidget(el)
    },

    routerRoot: '#app',
    _pageCache: new Map(),

    _currentAbort: null,
    _afterGoHooks: [],

    afterGo(fn) {
        if (typeof fn === 'function') {
            this._afterGoHooks.push(fn);
        }
        return this;
    },

    init(options = {}) {
        this.routerRoot = options.root ?? '#app';
        this.homePage   = options.home ?? 'component/home';
        this.basePath   = options.basePath ?? '';
        window.carbon   = this

        window.addEventListener('popstate', e => {
            const target = e.state?.page || this.homePage;
            this.go(target);
        });

        this.ready(() => this.go(this.homePage, true));
        return this;
    },

    async go(pageName, replace = false) {
        const root = document.querySelector(this.routerRoot);
        if (!root) {
            console.warn(`[CarbonUI] ルーターのマウント先要素("${this.routerRoot}")が見つかりません`);
            return this;
        }

        if (replace) {
            history.replaceState({ page: pageName }, '', `#${pageName}`);
        } else {
            history.pushState({ page: pageName }, '', `#${pageName}`);
        }

        // キャッシュ済みであればそれを使って高速表示
        if (this._pageCache.has(pageName)) {
            root.innerHTML = this._pageCache.get(pageName);
            this._executeScripts(root);
            this._afterGoHooks.forEach(fn => fn(pageName));
            return this;
        }

        // 進行中のfetchをキャンセル
        if (this._currentAbort) this._currentAbort.abort()
        const controller = new AbortController()
        this._currentAbort = controller

        // 初回はFetchでHTMLファイルを取得
        try {
            const res = await fetch(`${this.basePath}${pageName}.html`, { signal: controller.signal });
            if (!res.ok) throw new Error(`${pageName}.html の読み込みに失敗しました (${res.status})`);
            
            const html = await res.text();
            this._pageCache.set(pageName, html);
            root.innerHTML = html;
            this._executeScripts(root);
            this._afterGoHooks.forEach(fn => fn(pageName));
        } catch (err) {
            if (err.name === 'AbortError') return this;
            console.error('[CarbonUI] Routing Error:', err);
        }
        
        return this;
    },

    _executeScripts(element) {
        // innerHTMLで挿入されて無視されている <script> 要素をすべて手動で再評価(実行)する
        element.querySelectorAll('script').forEach(oldScript => {
            const newScript = document.createElement('script')
            Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value))
            newScript.appendChild(document.createTextNode(oldScript.innerHTML))
            oldScript.parentNode.replaceChild(newScript, oldScript)
        })
    },

    back() {
        history.back()
        return this
    },

    ready(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn)
        } else {
            fn()
        }
        return this
    }
}

export default carbon
export { CarbonWidget, CarbonEls }
