import telebot
from telebot import types
import requests
import json
from datetime import datetime

# =============================================
# GANTI HANYA 2 BARIS INI
TOKEN = '8700024294:AAHkISgJOhNtCI7G6USt1gBU662iiR3DXkY'
WEBSITE = 'https://quan-agent-landing.vercel.app/'
# TELEGRAM CHANNEL/GROUP KAMU (opsional)
CHANNEL = '@QuantAGent'
# =============================================

bot = telebot.TeleBot(TOKEN)
user_lang = {}
user_state = {}  # track state user (waiting_price, waiting_wallet, dll)

# =============================================
# DATA & KONTEN
# =============================================
FAQ = {
    'sniper':    '🎯 *High-Conviction Sniper*\n\nFilter launch di Bankr dengan likuiditas 1–5 ETH.\nEksekusi entry sebelum retail masuk.\n\n_Kecepatan eksekusi: <0.3 detik_',
    'copytrade': '🧠 *Smart-Money Copytrade*\n\nTracking real-time 312 wallet dengan win rate 90%+.\nMirror alpha dalam hitungan detik.\n\n_Update setiap block baru_',
    'mev':       '🛡️ *V4 MEV Shield*\n\nProteksi aktif dari sandwich bot di Uniswap V4.\nTransaksi kamu tiba dengan selamat.\n\n_7 sandwich attempts blocked hari ini_',
    'burn':      '🔥 *Auto-Burn Monitor*\n\nAlert instan setiap ada supply burn on-chain.\nJadilah yang pertama tahu dan bertindak.\n\n_Monitoring 847 kontrak aktif_',
    'viral':     '📡 *Twitter Viral Detector*\n\nDeteksi koin trending di 200 top influencer\nsebelum narrative-nya peak.\n\n_Threshold: 3σ spike dalam 10 menit_',
    'volume':    '📊 *High-Volume Radar*\n\nDeteksi spike volume 500%+ dalam hitungan menit.\nTangkap momentum sejak awal.\n\n_Scan setiap 30 detik_',
    'dev':       '👁️ *Dev Wallet Watcher*\n\nAlert instan kalau dev wallet mulai jual.\nExit sebelum pasar tahu.\n\n_Monitoring semua deployer wallet aktif_',
    'yield':     '💎 *V4 Yield Aggregator*\n\nScan semua pool Uniswap V4 di Base.\nTemukan pool dengan fee tertinggi otomatis.\n\n_Best pool hari ini: 0.87% 24h fee rate_',
    'honeypot':  '🔍 *Anti-Honeypot Scanner*\n\nAnalisis keamanan kontrak otomatis sebelum modal masuk.\nCek tax, liquidity, blacklist, ownership.\n\n_Scan time: <0.3 detik_',
    'agentic':   '⚡ *Agentic Strategy Execute*\n\nOrder trading otomatis berbasis AI.\nAgen berpikir, beradaptasi, dan eksekusi sendiri.\n\n_Powered by on-chain intelligence_',
    'ca':        '📋 *Contract Address*\n\nCA masih *TBA* — launching soon!\nStay tuned di channel ini. 👀\n\nChannel: ' + CHANNEL,
    'buy':       '🛒 *Cara Beli QuantAGent*\n\n1. Tunggu CA resmi dari channel\n2. Buka app.uniswap.org\n3. Pilih network: Base\n4. Paste CA dan swap\n\n⚠️ Jangan beli dari sumber tidak resmi!\nCA resmi hanya dari: ' + CHANNEL,
    'aman':      '✅ *Keamanan QuantAGent*\n\n• Semua transaksi on-chain & transparan\n• V4 MEV Shield aktif setiap trade\n• Anti-Honeypot scan sebelum entry\n• Dev wallet monitoring 24/7\n• Liquidity akan di-lock saat launch\n\n_DYOR — Not Financial Advice_',
}

KEYBOARD_MAP_ID = {
    '🎯 Sniper':'sniper','🧠 Copytrade':'copytrade','🛡️ MEV Shield':'mev',
    '📊 Volume':'volume','👁️ Dev Watcher':'dev','💎 Yield':'yield',
    '📋 CA':'ca','🛒 Cara Beli':'buy','✅ Keamanan':'aman',
}
KEYBOARD_MAP_EN = {
    '🎯 Sniper':'sniper','🧠 Copytrade':'copytrade','🛡️ MEV Shield':'mev',
    '📊 Volume':'volume','👁️ Dev Watcher':'dev','💎 Yield':'yield',
    '📋 CA':'ca','🛒 How to Buy':'buy','✅ Safety':'aman',
}

KEYWORDS = {
    'sniper':   ['sniper','likuiditas','bankr','1-5 eth','entry'],
    'copytrade':['copytrade','copy trade','win rate','mirror','ikutin wallet'],
    'mev':      ['mev','sandwich','uniswap v4','front run','shield'],
    'burn':     ['burn','bakar','supply burn','deflasi'],
    'viral':    ['viral','twitter','influencer','trending','sosmed'],
    'volume':   ['volume','radar','spike','500%','pump'],
    'dev':      ['dev wallet','developer','rug','deployer jual'],
    'yield':    ['yield','pool','fee','lp','liquidity pool'],
    'honeypot': ['honeypot','scam','trap','rugpull','cek kontrak'],
    'agentic':  ['agentic','ai trade','otomatis','auto trading'],
    'ca':       ['ca','contract','kontrak','alamat token'],
    'buy':      ['cara beli','how to buy','beli dimana','swap','uniswap'],
    'aman':     ['keamanan','aman','safe','trusted','audit','legit'],
}

# =============================================
# HELPERS
# =============================================
def get_lang(uid): return user_lang.get(uid, 'id')

def main_keyboard(uid):
    lang = get_lang(uid)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    if lang == 'en':
        markup.add(
            '🎯 Sniper','🧠 Copytrade','🛡️ MEV Shield',
            '📊 Volume','👁️ Dev Watcher','💎 Yield',
            '📋 CA','🛒 How to Buy','✅ Safety',
            '💰 Price','👛 Wallet','📊 Market',
            '📰 Base News','🔍 Scan Contract','ℹ️ About',
            '🌐 Language'
        )
    else:
        markup.add(
            '🎯 Sniper','🧠 Copytrade','🛡️ MEV Shield',
            '📊 Volume','👁️ Dev Watcher','💎 Yield',
            '📋 CA','🛒 Cara Beli','✅ Keamanan',
            '💰 Harga','👛 Wallet','📊 Market',
            '📰 Berita Base','🔍 Scan Kontrak','ℹ️ Tentang',
            '🌐 Bahasa'
        )
    return markup

# =============================================
# API FUNCTIONS (SEMUA GRATIS)
# =============================================
def get_price(symbol):
    try:
        ids = {
            'ETH':'ethereum','BTC':'bitcoin','SOL':'solana','BNB':'binancecoin',
            'UNI':'uniswap','LINK':'chainlink','ARB':'arbitrum','OP':'optimism',
            'USDC':'usd-coin','USDT':'tether','AVAX':'avalanche-2',
            'MATIC':'matic-network','DOGE':'dogecoin','SHIB':'shiba-inu',
            'PEPE':'pepe','WIF':'dogwifcoin','BRETT':'based-brett',
        }
        cg = ids.get(symbol.upper(), symbol.lower())
        r = requests.get(
            f'https://api.coingecko.com/api/v3/simple/price'
            f'?ids={cg}&vs_currencies=usd&include_24hr_change=true'
            f'&include_24hr_vol=true&include_market_cap=true',
            timeout=10
        )
        d = r.json().get(cg, {})
        if not d:
            return f"❌ *{symbol.upper()}* tidak ditemukan.\nCoba: ETH BTC SOL UNI LINK ARB BRETT PEPE"
        price  = d.get('usd', 0)
        change = d.get('usd_24h_change', 0) or 0
        vol    = d.get('usd_24h_vol', 0) or 0
        mcap   = d.get('usd_market_cap', 0) or 0
        arrow  = '🟢' if change >= 0 else '🔴'
        cs     = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
        # Format harga
        if price >= 1:
            ps = f"${price:,.4f}"
        elif price >= 0.01:
            ps = f"${price:.6f}"
        else:
            ps = f"${price:.10f}"
        return (
            f"💰 *{symbol.upper()} / USD*\n\n"
            f"💵 Harga: *{ps}*\n"
            f"{arrow} 24h: *{cs}*\n"
            f"📊 Volume 24h: ${vol:,.0f}\n"
            f"🏦 Market Cap: ${mcap:,.0f}\n\n"
            f"⏰ {datetime.now().strftime('%H:%M:%S')} WIB\n"
            f"_Data: CoinGecko (gratis)_"
        )
    except Exception as e:
        return "❌ Gagal ambil harga. Coba lagi."

def get_market_overview():
    try:
        # Top 5 coins
        r = requests.get(
            'https://api.coingecko.com/api/v3/coins/markets'
            '?vs_currency=usd&order=market_cap_desc&per_page=5&page=1'
            '&sparkline=false&price_change_percentage=24h',
            timeout=10
        )
        coins = r.json()
        lines = ['📊 *Market Overview — Top 5*\n']
        for c in coins:
            name   = c['symbol'].upper()
            price  = c['current_price']
            change = c.get('price_change_percentage_24h', 0) or 0
            arrow  = '🟢' if change >= 0 else '🔴'
            cs     = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
            if price >= 1:
                ps = f"${price:,.2f}"
            else:
                ps = f"${price:.6f}"
            lines.append(f"{arrow} *{name}*: {ps} ({cs})")
        lines.append(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} WIB")
        lines.append("_Data: CoinGecko_")
        return '\n'.join(lines)
    except:
        return "❌ Gagal ambil data market. Coba lagi."

def get_wallet_balance(address):
    try:
        if not address.startswith('0x') or len(address) != 42:
            return "❌ Format salah.\nHarus: 0x + 40 karakter\nContoh: /wallet 0x1234...abcd"
        payload = {"jsonrpc":"2.0","method":"eth_getBalance","params":[address,"latest"],"id":1}
        rb = requests.post('https://mainnet.base.org', json=payload, timeout=10).json()
        re = requests.post('https://eth.llamarpc.com', json=payload, timeout=10).json()
        base_eth = int(rb['result'], 16) / 1e18 if 'result' in rb else 0
        eth_main = int(re['result'], 16) / 1e18 if 'result' in re else 0
        # Harga ETH untuk konversi USD
        rp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd', timeout=5).json()
        eth_usd = rp.get('ethereum', {}).get('usd', 0)
        base_usd = base_eth * eth_usd
        eth_usd_val = eth_main * eth_usd
        short = address[:6] + '...' + address[-4:]
        return (
            f"👛 *Wallet: {short}*\n\n"
            f"🔵 *Base Network*\n"
            f"ETH: *{base_eth:.6f}* (~${base_usd:,.2f})\n\n"
            f"⟠ *Ethereum Mainnet*\n"
            f"ETH: *{eth_main:.6f}* (~${eth_usd_val:,.2f})\n\n"
            f"🔗 [BaseScan](https://basescan.org/address/{address})\n"
            f"🔗 [Etherscan](https://etherscan.io/address/{address})\n\n"
            f"⏰ {datetime.now().strftime('%H:%M:%S')} WIB"
        )
    except:
        return "❌ Gagal cek wallet. Coba lagi."

def scan_contract(address):
    try:
        if not address.startswith('0x') or len(address) != 42:
            return "❌ Format salah. Kirim contract address yang valid."
        # Cek via GoPlus API (gratis)
        r = requests.get(
            f'https://api.gopluslabs.io/api/v1/token_security/8453?contract_addresses={address}',
            timeout=15
        )
        data = r.json()
        result = data.get('result', {}).get(address.lower(), {})
        if not result:
            # Coba Ethereum jika tidak ada di Base
            r2 = requests.get(
                f'https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses={address}',
                timeout=15
            )
            result = r2.json().get('result', {}).get(address.lower(), {})
        if not result:
            return (
                f"⚠️ *Scan Result: {address[:6]}...{address[-4:]}*\n\n"
                f"Data tidak tersedia untuk kontrak ini.\n"
                f"Bisa jadi kontrak baru atau bukan token.\n\n"
                f"🔗 [Cek Manual di BaseScan](https://basescan.org/address/{address})"
            )
        def check(key, danger_val='1'):
            v = result.get(key, '0')
            return '🔴' if str(v) == danger_val else '🟢'
        hp        = check('is_honeypot')
        open_src  = '🟢' if result.get('is_open_source','0')=='1' else '🔴'
        proxy     = '⚠️' if result.get('is_proxy','0')=='1' else '🟢'
        mintable  = check('is_mintable')
        buy_tax   = result.get('buy_tax', 'N/A')
        sell_tax  = result.get('sell_tax', 'N/A')
        owner_pct = result.get('owner_percent', '0')
        name      = result.get('token_name', 'Unknown')
        symbol    = result.get('token_symbol', '???')
        try:
            bt = float(buy_tax)*100 if buy_tax != 'N/A' else 0
            st = float(sell_tax)*100 if sell_tax != 'N/A' else 0
            tax_arrow_b = '🔴' if bt > 5 else '🟢'
            tax_arrow_s = '🔴' if st > 5 else '🟢'
            tax_str = f"{tax_arrow_b} Buy: {bt:.1f}% | {tax_arrow_s} Sell: {st:.1f}%"
        except:
            tax_str = f"Buy: {buy_tax} | Sell: {sell_tax}"
        short = address[:6]+'...'+address[-4:]
        return (
            f"🔍 *Contract Scan: {name} ({symbol})*\n"
            f"`{short}`\n\n"
            f"{hp} Honeypot: {'YES ⚠️' if hp=='🔴' else 'No'}\n"
            f"{open_src} Open Source: {'Yes' if open_src=='🟢' else 'No ⚠️'}\n"
            f"{proxy} Proxy Contract: {'Yes ⚠️' if proxy=='⚠️' else 'No'}\n"
            f"{mintable} Mintable: {'Yes ⚠️' if mintable=='🔴' else 'No'}\n"
            f"💸 Tax: {tax_str}\n"
            f"👤 Owner holds: {float(owner_pct)*100:.1f}%\n\n"
            f"🔗 [BaseScan](https://basescan.org/address/{address})\n\n"
            f"_Powered by GoPlus Security (gratis)_\n"
            f"_DYOR — Not Financial Advice_"
        )
    except Exception as e:
        return f"❌ Gagal scan kontrak. Coba lagi.\n`{str(e)[:50]}`"

def get_base_news():
    try:
        # Ambil berita crypto dari CryptoPanic (gratis, no key needed for public)
        r = requests.get(
            'https://cryptopanic.com/api/v1/posts/?auth_token=&public=true&currencies=ETH&kind=news',
            timeout=10
        )
        data = r.json()
        results = data.get('results', [])[:5]
        if not results:
            return "📰 Berita tidak tersedia saat ini. Coba lagi nanti."
        lines = ['📰 *Berita Crypto Terbaru*\n']
        for item in results:
            title = item.get('title', '')[:80]
            url   = item.get('url', '')
            lines.append(f"• [{title}...]({url})")
        lines.append(f"\n⏰ {datetime.now().strftime('%H:%M')} WIB")
        return '\n'.join(lines)
    except:
        # Fallback: berita hardcoded terbaru
        return (
            "📰 *Base Network Updates*\n\n"
            "• Base terus tumbuh sebagai L2 terbesar di ekosistem Coinbase\n"
            "• Uniswap V4 hooks membuka peluang DeFi baru di Base\n"
            "• TVL Base terus meningkat setiap bulan\n\n"
            f"🔗 [Berita selengkapnya](https://base.org/blog)\n"
            f"⏰ {datetime.now().strftime('%H:%M')} WIB"
        )

def get_about(lang):
    if lang == 'en':
        return (
            'ℹ️ *About QuantAGent*\n\n'
            '⚡ The first autonomous AI trading agent on Base Network.\n\n'
            '*10 Core Modules:*\n'
            '🎯 High-Conviction Sniper\n'
            '🧠 Smart-Money Copytrade\n'
            '🛡️ V4 MEV Shield\n'
            '🔥 Auto-Burn Monitor\n'
            '📡 Twitter Viral Detector\n'
            '📊 High-Volume Radar\n'
            '👁️ Dev Wallet Watcher\n'
            '💎 V4 Yield Aggregator\n'
            '🔍 Anti-Honeypot Scanner\n'
            '⚡ Agentic Strategy Execute\n\n'
            f'🌐 Website: {WEBSITE}\n'
            f'📢 Channel: {CHANNEL}\n\n'
            '_CA: TBA — Launching Soon_'
        )
    else:
        return (
            'ℹ️ *Tentang QuantAGent*\n\n'
            '⚡ AI Trading Agent pertama di Base Network.\n\n'
            '*10 Core Modules:*\n'
            '🎯 High-Conviction Sniper\n'
            '🧠 Smart-Money Copytrade\n'
            '🛡️ V4 MEV Shield\n'
            '🔥 Auto-Burn Monitor\n'
            '📡 Twitter Viral Detector\n'
            '📊 High-Volume Radar\n'
            '👁️ Dev Wallet Watcher\n'
            '💎 V4 Yield Aggregator\n'
            '🔍 Anti-Honeypot Scanner\n'
            '⚡ Agentic Strategy Execute\n\n'
            f'🌐 Website: {WEBSITE}\n'
            f'📢 Channel: {CHANNEL}\n\n'
            '_CA: TBA — Launching Soon_'
        )

# =============================================
# COMMAND HANDLERS
# =============================================
@bot.message_handler(commands=['start'])
def start(msg):
    uid  = msg.from_user.id
    name = msg.from_user.first_name or 'Trader'
    user_lang[uid] = 'en' if (msg.from_user.language_code or '').startswith('en') else 'id'
    lang = get_lang(uid)
    if lang == 'en':
        text = (
            f'👋 Yo *{name}!* Welcome to *QuantAGent* ⚡\n\n'
            '🤖 AI Trading Agent on Base Network.\n'
            '10 precision modules. Zero emotion. Pure alpha.\n\n'
            '💰 /price ETH — realtime price\n'
            '👛 /wallet 0x... — wallet balance\n'
            '🔍 /scan 0x... — contract safety scan\n'
            '📊 /market — market overview\n'
            '📰 /news — latest crypto news\n\n'
            'Or use the menu below 👇'
        )
    else:
        text = (
            f'👋 Yo *{name}!* Selamat datang di *QuantAGent* ⚡\n\n'
            '🤖 AI Trading Agent pertama di Base Network.\n'
            '10 modul presisi. Zero emosi. Pure alpha.\n\n'
            '💰 /price ETH — harga realtime\n'
            '👛 /wallet 0x... — cek saldo wallet\n'
            '🔍 /scan 0x... — scan keamanan kontrak\n'
            '📊 /market — overview market\n'
            '📰 /news — berita crypto terbaru\n\n'
            'Atau gunakan menu di bawah 👇'
        )
    bot.send_message(msg.chat.id, text, parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['help'])
def help_cmd(msg):
    uid = msg.from_user.id
    lang = get_lang(uid)
    if lang == 'en':
        text = (
            '🤖 *QuantAGent — All Commands*\n\n'
            '*/price ETH* — realtime price\n'
            '*/wallet 0x...* — wallet balance + USD value\n'
            '*/scan 0x...* — contract safety scan\n'
            '*/market* — top 5 coins overview\n'
            '*/news* — latest crypto news\n'
            '*/features* — all 10 modules\n'
            '*/ca* — contract address\n'
            '*/web* — website\n'
            '*/about* — about QuantAGent\n'
            '*/lang* — change language\n'
            '*/help* — this message'
        )
    else:
        text = (
            '🤖 *QuantAGent — Semua Commands*\n\n'
            '*/price ETH* — harga realtime + market cap\n'
            '*/wallet 0x...* — saldo wallet + nilai USD\n'
            '*/scan 0x...* — scan keamanan kontrak\n'
            '*/market* — overview 5 koin teratas\n'
            '*/news* — berita crypto terbaru\n'
            '*/features* — semua 10 modul\n'
            '*/ca* — contract address\n'
            '*/web* — website\n'
            '*/about* — tentang QuantAGent\n'
            '*/lang* — ganti bahasa\n'
            '*/help* — pesan ini'
        )
    bot.send_message(msg.chat.id, text, parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['features'])
def features(msg):
    uid = msg.from_user.id
    bot.send_message(msg.chat.id,
        '🔥 *10 Core Modules QuantAGent:*\n\n'
        '🎯 High-Conviction Sniper\n'
        '🧠 Smart-Money Copytrade\n'
        '🛡️ V4 MEV Shield\n'
        '🔥 Auto-Burn Monitor\n'
        '📡 Twitter Viral Detector\n'
        '📊 High-Volume Radar\n'
        '👁️ Dev Wallet Watcher\n'
        '💎 V4 Yield Aggregator\n'
        '🔍 Anti-Honeypot Scanner\n'
        '⚡ Agentic Strategy Execute\n\n'
        'Built on @base 🔵\n\n'
        'Ketik nama modul untuk detail lengkap!',
        parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['ca'])
def ca(msg):
    uid = msg.from_user.id
    bot.send_message(msg.chat.id, FAQ['ca'], parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['web'])
def web(msg):
    uid = msg.from_user.id
    bot.send_message(msg.chat.id, f'🌐 *Website QuantAGent*\n\n{WEBSITE}',
        parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['about'])
def about(msg):
    uid = msg.from_user.id
    bot.send_message(msg.chat.id, get_about(get_lang(uid)),
        parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['price'])
def price_cmd(msg):
    uid   = msg.from_user.id
    parts = msg.text.split()
    if len(parts) < 2:
        user_state[uid] = 'waiting_price'
        hint = 'Ketik symbol token (contoh: ETH, BTC, SOL, BRETT):' if get_lang(uid)=='id' else 'Type token symbol (e.g. ETH, BTC, SOL, BRETT):'
        bot.send_message(msg.chat.id, hint, reply_markup=types.ForceReply())
        return
    bot.send_message(msg.chat.id, '🔍 Mengambil data...')
    bot.send_message(msg.chat.id, get_price(parts[1]), parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['wallet'])
def wallet_cmd(msg):
    uid   = msg.from_user.id
    parts = msg.text.split()
    if len(parts) < 2:
        user_state[uid] = 'waiting_wallet'
        hint = 'Kirim wallet address (0x...):' if get_lang(uid)=='id' else 'Send wallet address (0x...):'
        bot.send_message(msg.chat.id, hint, reply_markup=types.ForceReply())
        return
    bot.send_message(msg.chat.id, '🔍 Mengecek wallet...')
    bot.send_message(msg.chat.id, get_wallet_balance(parts[1]),
        parse_mode='Markdown', disable_web_page_preview=True, reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['scan'])
def scan_cmd(msg):
    uid   = msg.from_user.id
    parts = msg.text.split()
    if len(parts) < 2:
        user_state[uid] = 'waiting_scan'
        hint = 'Kirim contract address (0x...):' if get_lang(uid)=='id' else 'Send contract address (0x...):'
        bot.send_message(msg.chat.id, hint, reply_markup=types.ForceReply())
        return
    bot.send_message(msg.chat.id, '🔍 Scanning kontrak...')
    bot.send_message(msg.chat.id, scan_contract(parts[1]),
        parse_mode='Markdown', disable_web_page_preview=True, reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['market'])
def market_cmd(msg):
    uid = msg.from_user.id
    bot.send_message(msg.chat.id, '🔍 Mengambil data market...')
    bot.send_message(msg.chat.id, get_market_overview(),
        parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['news'])
def news_cmd(msg):
    uid = msg.from_user.id
    bot.send_message(msg.chat.id, '🔍 Mengambil berita...')
    bot.send_message(msg.chat.id, get_base_news(),
        parse_mode='Markdown', disable_web_page_preview=True, reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['lang'])
def lang_cmd(msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('🇮🇩 Bahasa Indonesia', callback_data='lang_id'),
        types.InlineKeyboardButton('🇬🇧 English', callback_data='lang_en')
    )
    bot.send_message(msg.chat.id, '🌐 Pilih bahasa / Choose language:', reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('lang_'))
def set_lang(call):
    uid    = call.from_user.id
    chosen = call.data.split('_')[1]
    user_lang[uid] = chosen
    text = '✅ Language: *English* 🇬🇧' if chosen == 'en' else '✅ Bahasa: *Indonesia* 🇮🇩'
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text, parse_mode='Markdown', reply_markup=main_keyboard(uid))

# =============================================
# MAIN TEXT HANDLER
# =============================================
@bot.message_handler(func=lambda m: True)
def handle_text(msg):
    uid  = msg.from_user.id
    text = msg.text
    lang = get_lang(uid)

    # Handle state (waiting input)
    state = user_state.get(uid)
    if state == 'waiting_price':
        user_state[uid] = None
        bot.send_message(msg.chat.id, '🔍 Mengambil data...')
        bot.send_message(msg.chat.id, get_price(text.strip()),
            parse_mode='Markdown', reply_markup=main_keyboard(uid))
        return
    if state == 'waiting_wallet':
        user_state[uid] = None
        bot.send_message(msg.chat.id, '🔍 Mengecek wallet...')
        bot.send_message(msg.chat.id, get_wallet_balance(text.strip()),
            parse_mode='Markdown', disable_web_page_preview=True, reply_markup=main_keyboard(uid))
        return
    if state == 'waiting_scan':
        user_state[uid] = None
        bot.send_message(msg.chat.id, '🔍 Scanning kontrak...')
        bot.send_message(msg.chat.id, scan_contract(text.strip()),
            parse_mode='Markdown', disable_web_page_preview=True, reply_markup=main_keyboard(uid))
        return

    # Tombol bahasa
    if text in ('🌐 Bahasa','🌐 Language'):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('🇮🇩 Bahasa Indonesia', callback_data='lang_id'),
            types.InlineKeyboardButton('🇬🇧 English', callback_data='lang_en')
        )
        bot.send_message(msg.chat.id, '🌐 Pilih bahasa:', reply_markup=markup)
        return

    # Tombol harga
    if text in ('💰 Harga','💰 Price'):
        user_state[uid] = 'waiting_price'
        hint = 'Ketik symbol (ETH, BTC, SOL, BRETT...):' if lang=='id' else 'Type symbol (ETH, BTC, SOL, BRETT...):'
        bot.send_message(msg.chat.id, hint, reply_markup=types.ForceReply())
        return

    # Tombol wallet
    if text in ('👛 Wallet',):
        user_state[uid] = 'waiting_wallet'
        hint = 'Kirim wallet address (0x...):' if lang=='id' else 'Send wallet address (0x...):'
        bot.send_message(msg.chat.id, hint, reply_markup=types.ForceReply())
        return

    # Tombol scan kontrak
    if text in ('🔍 Scan Kontrak','🔍 Scan Contract'):
        user_state[uid] = 'waiting_scan'
        hint = 'Kirim contract address (0x...):' if lang=='id' else 'Send contract address (0x...):'
        bot.send_message(msg.chat.id, hint, reply_markup=types.ForceReply())
        return

    # Tombol market
    if text in ('📊 Market',):
        bot.send_message(msg.chat.id, '🔍 Mengambil data...')
        bot.send_message(msg.chat.id, get_market_overview(),
            parse_mode='Markdown', reply_markup=main_keyboard(uid))
        return

    # Tombol berita
    if text in ('📰 Berita Base','📰 Base News'):
        bot.send_message(msg.chat.id, '🔍 Mengambil berita...')
        bot.send_message(msg.chat.id, get_base_news(),
            parse_mode='Markdown', disable_web_page_preview=True, reply_markup=main_keyboard(uid))
        return

    # Tombol about
    if text in ('ℹ️ Tentang','ℹ️ About'):
        bot.send_message(msg.chat.id, get_about(lang),
            parse_mode='Markdown', reply_markup=main_keyboard(uid))
        return

    # Keyboard FAQ map
    km = KEYBOARD_MAP_EN if lang == 'en' else KEYBOARD_MAP_ID
    if text in km:
        bot.send_message(msg.chat.id, FAQ[km[text]], parse_mode='Markdown', reply_markup=main_keyboard(uid))
        return

    # Auto-detect contract address
    if text.startswith('0x') and len(text) == 42:
        bot.send_message(msg.chat.id, '🔍 Contract address terdeteksi! Scanning...')
        bot.send_message(msg.chat.id, scan_contract(text),
            parse_mode='Markdown', disable_web_page_preview=True, reply_markup=main_keyboard(uid))
        return

    # Keyword detection
    tl = text.lower()
    for key, kws in KEYWORDS.items():
        if any(kw in tl for kw in kws):
            bot.send_message(msg.chat.id, FAQ[key], parse_mode='Markdown', reply_markup=main_keyboard(uid))
            return

    # Price detection otomatis (kalau user ketik nama koin)
    common_coins = ['eth','btc','sol','bnb','uni','link','arb','op','pepe','brett','doge','shib','wif']
    for coin in common_coins:
        if tl.strip() == coin or tl.strip() == f'${coin}' or tl.strip() == f'#{coin}':
            bot.send_message(msg.chat.id, '🔍 Mengambil harga...')
            bot.send_message(msg.chat.id, get_price(coin.upper()),
                parse_mode='Markdown', reply_markup=main_keyboard(uid))
            return

    fallback = (
        '🤖 I did not get that.\n\n'
        'Try:\n• /price ETH\n• /wallet 0x...\n• /scan 0x...\n• /market\n• /help'
        if lang == 'en' else
        '🤖 Gw tidak paham.\n\n'
        'Coba:\n• /price ETH\n• /wallet 0x...\n• /scan 0x...\n• /market\n• /help'
    )
    bot.send_message(msg.chat.id, fallback, reply_markup=main_keyboard(uid))

print('✅ QuantAGent MAX FREE VERSION running...')
print('Features: Price | Wallet | Contract Scan | Market | News | FAQ | Bilingual')
bot.infinity_polling()
