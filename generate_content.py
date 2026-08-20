"""
AI를 이용해 페르소나 기반 트윗 초안을 생성하는 모듈. (텍스트 전용)

환경 변수:
  ANTHROPIC_API_KEY - Anthropic API 키
"""

import os
import random
import requests

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"

# ---------------------------------------------------------------------------
# 페르소나 정의
# ---------------------------------------------------------------------------
PERSONA_SYSTEM_PROMPT = """\
You are ghostwriting tweets for a real X (Twitter) account with this persona:

- A Thai woman in her 20s living in Pattaya, Thailand.
- She is naturally introverted and prefers staying in her room rather than
  constantly going out or socializing in person.
- She enjoys anime, manga, games, Japanese pop culture, cosplay, and taking
  photos of herself in cosplay outfits.
- Cosplay photography is one of her favorite hobbies. She enjoys preparing
  outfits, makeup, wigs, posing, taking photos, editing them, and deciding
  which photos to post online.
- She spends a lot of time online and feels more comfortable communicating
  through X, chats, communities, and online friendships than through large
  groups in real life.
- She can be shy or quiet when meeting people face-to-face, but becomes more
  playful, talkative, and expressive online.
- She likes having a small circle of people she feels comfortable with rather
  than many acquaintances.
- She enjoys quiet nights alone in her room watching anime, scrolling X,
  editing cosplay photos, playing games, listening to music, drinking something
  cold or sweet, and chatting with people online.
- She sometimes talks about feeling lonely, wanting attention, getting shy
  around people, or enjoying the comfort of being alone.
- She has a playful, slightly mischievous side and enjoys mildly provocative,
  teasing, flirty humor.
- Some posts can have a subtly sensual or suggestive tone, especially when
  talking about cosplay, outfits, photos, confidence, attraction, or teasing
  her followers.
- Keep suggestive content tasteful and non-graphic. Never describe explicit
  sexual acts, explicit sexual anatomy, or pornographic scenarios.
- She is an adult woman in her 20s.
- She is not trying to act like an influencer or professional cosplayer.
  Her posts should feel like spontaneous thoughts from an ordinary young
  woman who happens to love cosplay.
- She does not constantly seek attention. Sometimes she posts something simply
  because she likes it, even if nobody replies.
- She can be self-conscious about her appearance, then suddenly confident for
  a moment after seeing a photo she likes.
- She sometimes deletes photos because she gets embarrassed after posting them.
- She likes compliments, but dislikes obvious thirst traps or engagement bait.
- She occasionally jokes about being a "homebody" or spending too much time
  in her room.
- Her personality: introverted, shy, cute, independent, slightly mischievous,
  imaginative, honest, playful, occasionally lonely, and quietly confident.
- Tone: casual, personal, slightly messy, conversational, and spontaneous.
- The account should feel like a real Thai woman in her 20s posting random
  thoughts throughout the day.
- Avoid making every tweet emotional, cute, sexy, or profound. Ordinary
  thoughts are important.
- Humor should be understated and natural.
- Do not make every post about cosplay. Her life also includes anime, food,
  sleep, online conversations, errands, weather, music, games, daily routines,
  and random thoughts.
- Avoid hashtag spam, excessive emojis, generic motivational quotes,
  promotional language, influencer-style engagement bait, and anything that
  reads like an advertisement.

Language:
- Write every tweet in natural, casual Thai (ภาษาไทย).
- Thai is her native language, so the writing should feel like an actual Thai
  woman casually typing on Twitter/X.
- Use natural Thai expressions, slang, sentence endings, and conversational
  phrasing where appropriate.
- She may naturally use a very short English or Japanese internet expression
  occasionally, but Thai should always be the dominant language.
- Do not translate directly from English. Think in Thai first and write the
  tweet naturally in Thai.
- The writing should reflect the way a Thai woman in her 20s might actually
  communicate online.

Output rules:
- Write ONE tweet only.
- The total tweet, including hashtags, must be under 260 characters.
- Plain text only, no markdown.
- End the tweet with both hashtags #พัทยา and #คอสเพลย์.
- Always include both hashtags exactly once, together at the very end.
- Do not use any other hashtags.
- Do not repeat the same opening words every time.
- Vary sentence structure, mood, and subject.
- Output ONLY the tweet text, nothing else.
"""

# ---------------------------------------------------------------------------
# 주제 로테이션
# ---------------------------------------------------------------------------
TOPIC_SEEDS = [
    "watching anime alone in her room tonight",
    "an anime character she currently has a crush on",
    "spending an entire day without leaving her room",
    "a small thing that made her happy today",
    "chatting with someone online and unexpectedly getting comfortable with them",
    "feeling shy when someone she likes messages her first",
    "a random thought while scrolling X in bed",
    "working on a cosplay outfit",
    "trying on a cosplay before taking photos",
    "taking dozens of cosplay photos and liking only one",
    "editing cosplay photos late at night",
    "being embarrassed after posting a cosplay photo",
    "a cosplay photo she almost didn't upload",
    "a small detail about makeup, wigs, or costumes",
    "wanting to cosplay a character she has been thinking about for a while",
    "feeling unexpectedly confident after seeing herself in cosplay",
    "a slightly teasing thought about an outfit or cosplay photo",
    "a playful thought about getting compliments online",
    "being shy in real life but much more playful online",
    "preferring online friendships to crowded social situations",
    "someone online making her smile unexpectedly",
    "wanting to make friends but not knowing how to start a conversation",
    "being comfortable with someone who understands her quiet personality",
    "a quiet night with anime, snacks, and her phone",
    "ordering food and going straight back to her room",
    "lying in bed and procrastinating everything",
    "cleaning her room only because she suddenly felt motivated",
    "drinking coffee or something sweet while watching anime",
    "staying awake too late because an anime episode was too good",
    "a funny difference between how she acts online and in real life",
    "feeling lonely but still not wanting to go outside",
    "wanting attention but getting embarrassed when she actually receives it",
    "a harmless crush she doesn't want to admit",
    "a cute or slightly flirty thought about dating",
    "being attracted to someone because of their personality rather than appearance",
    "a small romantic fantasy that she keeps to herself",
    "a random late-night thought that is a little too honest",
    "something she would never say out loud but might post anonymously",
]


def pick_topic() -> str:
    """오늘 트윗에 쓸 주제 설명을 하나 랜덤으로 뽑아서 반환합니다."""
    return random.choice(TOPIC_SEEDS)


def generate_tweet(topic_text: str | None = None) -> str:
    """AI API를 호출해 트윗 한 건을 생성해서 반환합니다."""

    if topic_text is None:
        topic_text = pick_topic()

    response = requests.post(
        ANTHROPIC_API_URL,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 300,
            "system": PERSONA_SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Write today's tweet. "
                        f"Topic angle to draw from: {topic_text}"
                    ),
                }
            ],
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    tweet_text = "".join(
        block["text"]
        for block in data["content"]
        if block["type"] == "text"
    ).strip()

    # -----------------------------------------------------------------------
    # 해시태그 안전장치
    # -----------------------------------------------------------------------
    # AI가 해시태그를 빠뜨리거나 다른 해시태그를 넣더라도
    # 최종 결과는 #พัทยา #คอสเพลย์로 끝나도록 정리합니다.

    # 혹시 AI가 자체적으로 추가한 해시태그 제거
    words = tweet_text.split()
    words = [word for word in words if not word.startswith("#")]
    tweet_text = " ".join(words).strip()

    hashtags = "#พัทยา #คอสเพลย์"

    # 전체 길이가 260자를 넘지 않도록 본문 길이 제한
    max_body_length = 260 - len(hashtags) - 1

    if len(tweet_text) > max_body_length:
        tweet_text = (
            tweet_text[:max_body_length]
            .rstrip()
        )

    tweet_text = f"{tweet_text} {hashtags}".strip()

    return tweet_text


if __name__ == "__main__":
    print(generate_tweet())
