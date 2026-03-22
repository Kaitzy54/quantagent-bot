import telebot
from telebot import types

# =============================================
# GANTI TOKEN DI SINI DENGAN TOKEN BOTFATHER
TOKEN = 'ISI_TOKEN_BOTFATHER_KAMU_DI_SINI'
# GANTI LINK WEBSITE VERCEL KAMU
WEBSITE = 'https://quantagent.vercel.app'
# =============================================

bot = telebot.TeleBot(TOKEN)
user_lang = {}

CONTENT = {
    'id': {
        'welcome': (
            '👋 Yo *{name}!* Selamat datang di *QuantAGent* ⚡\n\n'
            '🤖 AI Trading Agent pertama di Base Network.\n'
            '10 modul presisi. Zero emosi. Pure alpha.\n\n'
            'Pilih menu di bawah atau ketik pertanyaan kamu:'
        ),
        'help': (
            '🤖 *QuantAGent Bot — Bantuan*\n\n'
            '/start — Menu utama\n'
            '/features — Semua 10 modul\n'
            '/ca — Contract address\n'
            '/web — Link website\n'
            '/lang — Ganti bahasa\n'
            '/help — Bantuan\n\n'
            'Atau langsung ketik pertanyaan kamu!'
        ),
        'features': (
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
            'Dibangun khusus di @base 🔵'
        ),
        'ca': '📋 *Contract Address*\n\nCA masih *TBA* — launching soon!\nStay tuned di channel ini. 👀',
        'web': '🌐 *Website QuantAGent*\n\n{website}',
        'not_found': '🤖 Hmm, gw belum paham itu.\n\nCoba tanya: sniper, copytrade, MEV, volume, CA, cara beli\n\nAtau ketik /help',
        'lang_changed': '✅ Bahasa diubah ke *Bahasa Indonesia*',
        'pick_lang': '🌐 Pilih bahasa kamu:',
        'faq': {
            'sniper': '🎯 *High-Conviction Sniper*\n\nFilter launch di Bankr dengan likuiditas 1–5 ETH.\nEksekusi entry sebelum retail masuk.',
            'copytrade': '🧠 *Smart-Money Copytrade*\n\nTracking real-time wallet dengan win rate 90%+.\nMirror alpha dalam hitungan detik.',
            'mev': '🛡️ *V4 MEV Shield*\n\nProteksi aktif dari sandwich bot di Uniswap V4.\nTransaksi kamu tiba dengan selamat.',
            'burn': '🔥 *Auto-Burn Monitor*\n\nAlert instan setiap ada supply burn on-chain.\nJadilah yang pertama tahu.',
            'viral': '📡 *Twitter Viral Detector*\n\nDeteksi koin trending di kalangan top influencer\nsebelum narrative-nya peak.',
            'volume': '📊 *High-Volume Radar*\n\nDeteksi spike volume 500%+ dalam hitungan menit.\nTangkap momentum sejak awal.',
            'dev': '👁️ *Dev Wallet Watcher*\n\nAlert instan kalau dev wallet mulai jual.\nExit sebelum pasar tahu.',
            'yield': '💎 *V4 Yield Aggregator*\n\nScan semua pool Uniswap V4 di Base.\nTemukan pool dengan fee tertinggi otomatis.',
            'honeypot': '🔍 *Anti-Honeypot Scanner*\n\nAnalisis keamanan kontrak otomatis.\nTidak ada modal masuk sebelum kontrak aman.',
            'agentic': '⚡ *Agentic Strategy Execute*\n\nOrder trading otomatis berbasis AI.\nAgen berpikir, beradaptasi, dan eksekusi sendiri.',
            'ca': '📋 *Contract Address*\n\nCA masih *TBA* — launching soon!\nStay tuned di sini. 👀',
            'buy': '🛒 *Cara Beli*\n\nCA masih TBA. Tunggu pengumuman resmi!\nJangan beli dari sumber tidak resmi.',
            'aman': '✅ *Keamanan QuantAGent*\n\nSemua transaksi on-chain dan transparan.\nAnti-honeypot scanner aktif sebelum setiap trade.\nV4 MEV Shield melindungi dari sandwich bot.',
        },
        'keywords': {
            'sniper': ['sniper', 'likuiditas', 'launch', 'bankr'],
            'copytrade': ['copytrade', 'copy', 'wallet', 'win rate', 'mirror'],
            'mev': ['mev', 'sandwich', 'uniswap', 'shield'],
            'burn': ['burn', 'bakar', 'supply'],
            'viral': ['viral', 'twitter', 'influencer', 'trending'],
            'volume': ['volume', 'radar', 'spike', 'lonjakan'],
            'dev': ['dev', 'developer', 'jual', 'rug'],
            'yield': ['yield', 'pool', 'fee'],
            'honeypot': ['honeypot', 'scam', 'scanner', 'kontrak'],
            'agentic': ['agentic', 'ai', 'otomatis', 'strategi'],
            'ca': ['ca', 'contract', 'alamat'],
            'buy': ['beli', 'buy', 'cara beli'],
            'aman': ['keamanan', 'aman', 'security'],
        },
        'keyboard': ['🎯 Sniper','🧠 Copytrade','🛡️ MEV Shield','📊 Volume Radar','👁️ Dev Watcher','💎 Yield','📋 Contract Address','🛒 Cara Beli','✅ Keamanan','🌐 Ganti Bahasa'],
        'keyboard_map': {'🎯 Sniper':'sniper','🧠 Copytrade':'copytrade','🛡️ MEV Shield':'mev','📊 Volume Radar':'volume','👁️ Dev Watcher':'dev','💎 Yield':'yield','📋 Contract Address':'ca','🛒 Cara Beli':'buy','✅ Keamanan':'aman'},
    },
    'en': {
        'welcome': (
            '👋 Yo *{name}!* Welcome to *QuantAGent* ⚡\n\n'
            '🤖 The first AI Trading Agent on Base Network.\n'
            '10 precision modules. Zero emotion. Pure alpha.\n\n'
            'Pick a menu below or type your question:'
        ),
        'help': (
            '🤖 *QuantAGent Bot — Help*\n\n'
            '/start — Main menu\n'
            '/features — All 10 modules\n'
            '/ca — Contract address\n'
            '/web — Website link\n'
            '/lang — Change language\n'
            '/help — Help\n\n'
            'Or just type your question!'
        ),
        'features': (
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
            'Built natively on @base 🔵'
        ),
        'ca': '📋 *Contract Address*\n\nCA is *TBA* — launching soon!\nStay tuned here for updates. 👀',
        'web': '🌐 *QuantAGent Website*\n\n{website}',
        'not_found': '🤖 Hmm, I did not get that.\n\nTry asking about: sniper, copytrade, MEV, volume, CA, how to buy\n\nOr type /help',
        'lang_changed': '✅ Language changed to *English*',
        'pick_lang': '🌐 Choose your language:',
        'faq': {
            'sniper': '🎯 *High-Conviction Sniper*\n\nFilters Bankr launches with 1–5 ETH liquidity.\nExecutes entry before retail discovers the play.',
            'copytrade': '🧠 *Smart-Money Copytrade*\n\nReal-time tracking of 90%+ win-rate wallets.\nMirror alpha in seconds, not minutes.',
            'mev': '🛡️ *V4 MEV Shield*\n\nActive protection against sandwich bots on Uniswap V4.\nYour transactions arrive intact.',
            'burn': '🔥 *Auto-Burn Monitor*\n\nInstant on-chain alerts when supply burns happen.\nBe first to act on deflationary events.',
            'viral': '📡 *Twitter Viral Detector*\n\nDetects coins trending among top influencers\nbefore the narrative peaks.',
            'volume': '📊 *High-Volume Radar*\n\nIdentifies 500%+ volume spikes within minutes.\nCatch momentum at inception, not after.',
            'dev': '👁️ *Dev Wallet Watcher*\n\nInstant alert when dev wallets start selling.\nExit before the rest of the market knows.',
            'yield': '💎 *V4 Yield Aggregator*\n\nScans all Uniswap V4 pools on Base.\nFinds the highest fee-generating positions automatically.',
            'honeypot': '🔍 *Anti-Honeypot Scanner*\n\nAutomated contract safety analysis.\nNo capital enters before the contract is verified safe.',
            'agentic': '⚡ *Agentic Strategy Execute*\n\nAI-driven automated trading orders.\nThe agent thinks, adapts, and executes on its own.',
            'ca': '📋 *Contract Address*\n\nCA is *TBA* — launching soon!\nStay tuned here. 👀',
            'buy': '🛒 *How to Buy*\n\nCA is TBA. Wait for the official announcement!\nDo not buy from unofficial sources.',
            'aman': '✅ *QuantAGent Safety*\n\nAll transactions are on-chain and transparent.\nAnti-honeypot scanner active before every trade.\nV4 MEV Shield protects against sandwich bots.',
        },
        'keywords': {
            'sniper': ['sniper', 'liquidity', 'launch', 'bankr'],
            'copytrade': ['copytrade', 'copy', 'wallet', 'win rate', 'mirror'],
            'mev': ['mev', 'sandwich', 'uniswap', 'shield'],
            'burn': ['burn', 'supply', 'deflationary'],
            'viral': ['viral', 'twitter', 'influencer', 'trending'],
            'volume': ['volume', 'radar', 'spike'],
            'dev': ['dev', 'developer', 'sell', 'rug'],
            'yield': ['yield', 'pool', 'fee', 'aggregator'],
            'honeypot': ['honeypot', 'scam', 'scanner', 'contract'],
            'agentic': ['agentic', 'ai', 'automated', 'strategy'],
            'ca': ['ca', 'contract', 'address'],
            'buy': ['buy', 'purchase', 'how to buy'],
            'aman': ['safety', 'safe', 'secure', 'security'],
        },
        'keyboard': ['🎯 Sniper','🧠 Copytrade','🛡️ MEV Shield','📊 Volume Radar','👁️ Dev Watcher','💎 Yield','📋 Contract Address','🛒 How to Buy','✅ Safety','🌐 Change Language'],
        'keyboard_map': {'🎯 Sniper':'sniper','🧠 Copytrade':'copytrade','🛡️ MEV Shield':'mev','📊 Volume Radar':'volume','👁️ Dev Watcher':'dev','💎 Yield':'yield','📋 Contract Address':'ca','🛒 How to Buy':'buy','✅ Safety':'aman'},
    }
}

def get_lang(uid): return user_lang.get(uid, 'id')
def get_content(uid): return CONTENT[get_lang(uid)]
def main_keyboard(uid):
    c = get_content(uid)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(*c['keyboard'])
    return markup

def get_faq_reply(uid, text):
    c = get_content(uid)
    text_lower = text.lower()
    for key, keywords in c['keywords'].items():
        for kw in keywords:
            if kw in text_lower:
                return c['faq'].get(key)
    return None

@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.from_user.id
    name = msg.from_user.first_name or 'Trader'
    lang_code = msg.from_user.language_code or 'id'
    user_lang[uid] = 'en' if lang_code.startswith('en') else 'id'
    c = get_content(uid)
    bot.send_message(msg.chat.id, c['welcome'].format(name=name), parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['help'])
def help_cmd(msg):
    uid = msg.from_user.id
    c = get_content(uid)
    bot.send_message(msg.chat.id, c['help'], parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['features'])
def features(msg):
    uid = msg.from_user.id
    c = get_content(uid)
    bot.send_message(msg.chat.id, c['features'], parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['ca'])
def ca(msg):
    uid = msg.from_user.id
    c = get_content(uid)
    bot.send_message(msg.chat.id, c['ca'], parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['web'])
def web(msg):
    uid = msg.from_user.id
    c = get_content(uid)
    bot.send_message(msg.chat.id, c['web'].format(website=WEBSITE), parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(commands=['lang'])
def lang_cmd(msg):
    uid = msg.from_user.id
    c = get_content(uid)
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('🇮🇩 Bahasa Indonesia', callback_data='lang_id'),
        types.InlineKeyboardButton('🇬🇧 English', callback_data='lang_en')
    )
    bot.send_message(msg.chat.id, c['pick_lang'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_lang(call):
    uid = call.from_user.id
    chosen = call.data.split('_')[1]
    user_lang[uid] = chosen
    c = get_content(uid)
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, c['lang_changed'], parse_mode='Markdown', reply_markup=main_keyboard(uid))

@bot.message_handler(func=lambda m: True)
def handle_text(msg):
    uid = msg.from_user.id
    text = msg.text
    c = get_content(uid)
    if text in ('🌐 Ganti Bahasa', '🌐 Change Language'):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('🇮🇩 Bahasa Indonesia', callback_data='lang_id'),
            types.InlineKeyboardButton('🇬🇧 English', callback_data='lang_en')
        )
        bot.send_message(msg.chat.id, c['pick_lang'], reply_markup=markup)
        return
    if text in c['keyboard_map']:
        key = c['keyboard_map'][text]
        reply = c['faq'].get(key)
        if reply:
            bot.send_message(msg.chat.id, reply, parse_mode='Markdown', reply_markup=main_keyboard(uid))
            return
    reply = get_faq_reply(uid, text)
    if reply:
        bot.send_message(msg.chat.id, reply, parse_mode='Markdown', reply_markup=main_keyboard(uid))
    else:
        bot.send_message(msg.chat.id, c['not_found'], reply_markup=main_keyboard(uid))

print('✅ QuantAGent Bot (ID + EN) is running...')
bot.infinity_polling()
