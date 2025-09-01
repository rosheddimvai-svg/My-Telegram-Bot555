import logging
import random
import string
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# আপনার বট টোকেন এবং প্রাইভেট চ্যানেলের আইডি এখানে দিন
TOKEN = "8495166192:AAF4equQDsT9iCWS2IQ-x63il9IHbEi4XpY"
CHANNEL_ID_ONE = -1002632355234
CHANNEL_ID_TWO = -1002323042564

# Logging সেটআপ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# প্রতিটি ব্যবহারকারীর অবস্থা ট্র্যাক করার জন্য একটি ডিকশনারি
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """স্টার্ট (/start) কমান্ড হ্যান্ডেল করে।"""
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name if update.effective_user.first_name else "বন্ধু"

    user_states[user_id] = {"step": "waiting_for_uid"}
    
    start_message = (
        f"**আসসালামু আলাইকুম, {first_name} ভাই!**\n\n"
        f"আমাদের বটটিতে আপনাকে স্বাগতম। আমাদের বিশেষ **DK WIN হ্যাকটি** ব্যবহার করে আপনি গেম থেকে অনেক বেশি ইনকাম করতে পারবেন এবং খুব সহজেই আপনার স্বপ্নের লক্ষ্য পূরণ করতে পারবেন। আমাদের বটটি ব্যবহার করা খুবই সহজ।\n\n"
        f"শুরু করার জন্য, অনুগ্রহ করে আপনার **DK WIN গেমের ইউআইডি (UID)** টি পাঠান।\n\n"
        f"⚠️ **গুরুত্বপূর্ণ:** আপনার ইউআইডি শুধুমাত্র সংখ্যা দিয়ে গঠিত হতে হবে। অন্য কোনো অক্ষর ব্যবহার করা যাবে না।"
    )
    await update.message.reply_text(start_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """মেসেজ হ্যান্ডেল করে।"""
    user = update.effective_user
    user_id = user.id
    
    current_state = user_states.get(user_id, {})
    current_step = current_state.get("step")

    if current_step == "waiting_for_uid":
        user_uid = update.message.text
        
        # নিশ্চিত করা যে UID শুধুমাত্র সংখ্যা দিয়ে গঠিত
        if not user_uid.isdigit():
            await update.message.reply_text("দুঃখিত! আপনার ইউআইডিটি শুধুমাত্র সংখ্যা দিয়ে গঠিত হতে হবে। অনুগ্রহ করে সঠিক ইউআইডিটি আবার পাঠান।")
            return
        
        user_states[user_id]["uid"] = user_uid
        user_states[user_id]["step"] = "waiting_for_username"

        username_prompt = (
            "✅ **সফলভাবে জমা পড়েছে!** ✅\n\n"
            "এখন অনুগ্রহ করে হ্যাকের ভিতর প্রবেশ করুন। সেখানে আপনার যে **ইউজারনেমটি** দেখতে পাবেন, সেটি আমাদেরকে পাঠান।"
        )
        await update.message.reply_text(username_prompt)
        
    elif current_step == "waiting_for_username":
        user_input_username = update.message.text
        
        user_states[user_id]["game_username"] = user_input_username
        
        # একটি র্যান্ডম অ্যাপ্রুভাল কি তৈরি করা হচ্ছে
        random_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        user_uid = user_states[user_id]["uid"]
        
        response_message = (
            f"✅ **আপনার আবেদনটি সফলভাবে জমা পড়েছে!** ✅\n\n"
            f"আপনার আবেদনটি এখন আমাদের টেস্টিং টিমের কাছে পাঠানো হয়েছে। দয়া করে একটু অপেক্ষা করুন। কিছুক্ষণের মধ্যেই আপনাকে অ্যাপ্রুভ দেয়া হবে এবং আপনি আপনার হ্যাকটি ব্যবহার করতে পারবেন।"
        )
        
        # অ্যাপ্রুভাল কি এর জন্য কপি বাটন তৈরি করা
        key_button = [[InlineKeyboardButton(text=f"কপি করতে ক্লিক করুন: {random_key}", url=f"https://t.me/share/url?url={random_key}")]]
        key_markup = InlineKeyboardMarkup(key_button)

        await update.message.reply_text(response_message, reply_markup=key_markup)

        # কনফার্ম এবং রিজেক্ট বাটন তৈরি করা
        keyboard = [
            [
                InlineKeyboardButton("কনফার্ম", callback_data=f"CONFIRM_{user_id}_{random_key}"),
                InlineKeyboardButton("রিজেক্ট", callback_data=f"REJECT_{user_id}_{random_key}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # প্রাইভেট চ্যানেলে (চ্যানেল ১) তথ্য এবং বাটন পাঠানো হচ্ছে
        bot = Bot(TOKEN)
        message_to_channel_one = (
            f"**নতুন ইউজার:**\n"
            f"ইউজার আইডি: `{user_id}`\n"
            f"ইউজারনেম: @{user.username if user.username else 'N/A'}\n"
            f"ইউআইডি: `{user_uid}`\n"
            f"গেম ইউজারনেম: `{user_input_username}`\n"
            f"অ্যাপ্রুভাল কি: `{random_key}`"
        )
        
        await bot.send_message(
            chat_id=CHANNEL_ID_ONE, 
            text=message_to_channel_one, 
            reply_markup=reply_markup
        )

        # ব্যবহারকারীর অবস্থা রিসেট করা
        del user_states[user_id]
        
    else:
        await update.message.reply_text("দয়া করে /start কমান্ডটি ব্যবহার করুন।")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ইনলাইন বাটনে ক্লিক হ্যান্ডেল করে।"""
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    action = data[0]
    
    if action == "CONFIRM":
        user_id = data[1]
        key = data[2]
        
        # মূল মেসেজ থেকে সম্পূর্ণ তথ্য বের করা
        original_message_text = query.message.text
        
        # কনফার্ম বাটন চাপলে দ্বিতীয় চ্যানেলে একটি নতুন কনফার্ম বাটন সহ সম্পূর্ণ তথ্য পাঠানো হচ্ছে
        bot = Bot(TOKEN)
        
        keyboard_two = [[InlineKeyboardButton("চূড়ান্ত কনফার্ম", callback_data=f"FINAL_CONFIRM_{user_id}_{key}")]]
        reply_markup_two = InlineKeyboardMarkup(keyboard_two)
        
        await bot.send_message(
            chat_id=CHANNEL_ID_TWO, 
            text=original_message_text,
            reply_markup=reply_markup_two
        )
        
        # প্রথম চ্যানেলের মেসেজ আপডেট করা হচ্ছে
        await query.edit_message_text(text=f"✅ এই অনুরোধটি কনফার্ম করা হয়েছে। চূড়ান্ত অ্যাপ্রুভালের জন্য দ্বিতীয় চ্যানেলে পাঠানো হয়েছে।")

    elif action == "REJECT":
        # রিজেক্ট বাটন চাপলে প্রথম চ্যানেলের মেসেজ আপডেট করা হচ্ছে
        await query.edit_message_text(text=f"❌ এই অনুরোধটি রিজেক্ট করা হয়েছে।")

    elif action == "FINAL_CONFIRM":
        user_id = data[1]
        key = data[2]
        
        # দ্বিতীয় চ্যানেলের চূড়ান্ত কনফার্ম বাটন চাপলে ইউজারকে নোটিফিকেশন পাঠানো হচ্ছে
        bot = Bot(TOKEN)
        
        # ইউজারকে নোটিফিকেশন পাঠানো হচ্ছে
        notification_message = (
            f"🎉 **অভিনন্দন!** 🎉\n\n"
            f"আপনার হ্যাকটি সফলভাবে অ্যাপ্রুভ হয়েছে। এখন আপনি আপনার হ্যাকটি লগইন করতে পারবেন।\n\n"
            f"আপনার সিক্রেট কি: `{key}`\n\n"
            f"এই কি দিয়ে আপনার হ্যাকটি লগইন করুন।"
        )
        # অ্যাপ্রুভাল কি এর জন্য কপি বাটন যোগ করা
        copy_button = [[InlineKeyboardButton(text=f"কপি করতে ক্লিক করুন: {key}", url=f"https://t.me/share/url?url={key}")]]
        copy_markup = InlineKeyboardMarkup(copy_button)
        
        await bot.send_message(chat_id=user_id, text=notification_message, reply_markup=copy_markup)
        
        # দ্বিতীয় চ্যানেলের মেসেজ আপডেট করা হচ্ছে
        await query.edit_message_text(text=f"✅ এই ইউজারকে অ্যাপ্রুভাল দেওয়া হয়েছে।")

def main() -> None:
    """বট শুরু করে।"""
    application = Application.builder().token(TOKEN).build()

    # কমান্ড এবং মেসেজ হ্যান্ডলার যোগ করা
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    # বট পোলিং শুরু করা
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()