import math
import random
import tkinter as tk


WINDOW_W = 260
WINDOW_H = 60
POINT_COUNT = 160
POPUP_INTERVAL_MS = 120
MOVE_DURATION_MS = 1500
FRAME_MS = 16
FINAL_HOLD_MS = 16000

TITLE_TEXT = "心之所向  爱之所往"

PHRASE_SEEDS = [
    "多喝水哦", "保持好心情", "好好爱自己", "别熬夜了", "今天也要加油",
    "我想你了", "想抱抱你", "等你回家", "有我在呢", "慢慢来就好",
    "记得吃饭呀", "别太累了", "今天辛苦啦", "你已经很棒了", "我一直都在",
    "不开心就抱抱", "想听你说话", "晚点也没关系", "我陪着你呀", "不要硬撑",
    "把烦恼给我", "早点休息呀", "梦里也见你", "你笑起来最好看", "今天也喜欢你",
    "想和你散步", "给你一点甜", "要照顾好自己", "天气凉多穿点", "我在想你呢",
    "见到你就开心", "想牵你的手", "你是我的偏爱", "抱抱我的小朋友", "别怕我在",
    "心情不好找我", "想把温柔给你", "你不用逞强", "我永远站你这边", "今晚早点睡",
    "给你充充电", "想陪你发呆", "喜欢你的认真", "喜欢你的可爱", "你值得被好好爱",
    "把开心分你一半", "我会慢慢陪你", "今天也很想见你", "你一出现就安心", "别偷偷难过",
    "累了就靠一靠", "我来哄你呀", "亲亲就不累啦", "想给你热奶茶", "我最偏心你",
    "我会记得你的好", "你不用完美", "你怎样都可爱", "想听你碎碎念", "被你需要很开心",
    "给你满格安全感", "今天要被宠爱", "你是我的小确幸", "喜欢和你在一起", "想和你看日落",
    "我会好好珍惜你", "你负责开心就好", "想把好运给你", "所有温柔都给你", "想陪你很久很久",
    "你在我心尖上", "不许自己偷偷委屈", "有事第一时间找我", "今晚月色很适合想你", "抱一下就好了",
    "我喜欢现在的你", "也喜欢明天的你", "想成为你的依靠", "我的温柔只给你", "每天都想靠近你",
    "你是我认真选择的人", "我们慢慢来", "我会一直偏爱你", "想把快乐攒给你", "今天也要被我喜欢",
    "你的消息我都期待", "不忙也想找你", "想和你一起吃饭", "我会接住你的情绪", "你不用一个人扛",
    "我在你身后呢", "给你一个大大的抱抱", "你值得所有温柔", "想把星星送给你", "我喜欢你很久很久",
]

PHRASE_PREFIXES = [
    "今天", "明天", "每一天", "想你的时候", "见到你的时候", "下班以后", "睡觉以前", "醒来以后",
    "天气变冷时", "你累了的时候", "你难过的时候", "你开心的时候", "想见你的时候", "靠近你的时候",
]

PHRASE_SUFFIXES = [
    "都想抱抱你", "都想陪着你", "都把温柔给你", "都希望你开心", "都想听你说话",
    "都觉得你很可爱", "都想牵你的手", "都想把好运给你", "都想认真爱你", "都想给你安全感",
    "都想和你多待一会", "都想把甜甜的给你", "都想让你少一点委屈", "都想和你一起慢慢来",
]

BG_COLORS = [
    "#ffd6e8", "#ffe0cc", "#fff0b8", "#dfffe2", "#d7f5ff", "#ead7ff",
    "#ffb6c1", "#ffa07a", "#f0e68c", "#98fb98", "#87ceeb", "#dda0dd",
    "#f8c8dc", "#c8f7dc", "#cce5ff", "#ffe4b5", "#e6e6fa", "#f5deb3",
]

TEXT_COLORS = ["#4a2040", "#4a2c15", "#263b24", "#18394a", "#40235f"]


def ease_out_cubic(progress):
    return 1 - (1 - progress) ** 3


def make_text_pool(count):
    phrases = list(dict.fromkeys(PHRASE_SEEDS))
    for prefix in PHRASE_PREFIXES:
        for suffix in PHRASE_SUFFIXES:
            phrase = f"{prefix}{suffix}"
            if phrase not in phrases:
                phrases.append(phrase)
            if len(phrases) >= count:
                random.shuffle(phrases)
                return phrases[:count]
    random.shuffle(phrases)
    return phrases[:count]


def generate_heart_points(num_points, screen_w, screen_h):
    raw_points = []
    for i in range(num_points):
        t = 2 * math.pi * i / num_points
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        raw_points.append((x, y))

    min_x = min(x for x, _ in raw_points)
    max_x = max(x for x, _ in raw_points)
    min_y = min(y for _, y in raw_points)
    max_y = max(y for _, y in raw_points)

    margin_x = 30
    margin_y = 42
    usable_w = max(1, screen_w - WINDOW_W - margin_x * 2)
    usable_h = max(1, screen_h - WINDOW_H - margin_y * 2)
    scale = min(usable_w / (max_x - min_x), usable_h / (max_y - min_y))
    heart_w = (max_x - min_x) * scale
    heart_h = (max_y - min_y) * scale
    base_x = (screen_w - heart_w - WINDOW_W) / 2
    base_y = (screen_h - heart_h - WINDOW_H) / 2

    points = []
    for x, y in raw_points:
        px = int(base_x + (x - min_x) * scale)
        py = int(base_y + heart_h - (y - min_y) * scale)
        px = max(0, min(px, screen_w - WINDOW_W))
        py = max(0, min(py, screen_h - WINDOW_H))
        points.append((px, py))
    return points


def random_start_point(index, screen_w, screen_h):
    side = index % 4
    if side == 0:
        return random.randint(0, screen_w - WINDOW_W), screen_h - WINDOW_H - random.randint(0, 90)
    if side == 1:
        return screen_w - WINDOW_W - random.randint(0, 90), random.randint(0, screen_h - WINDOW_H)
    if side == 2:
        return random.randint(0, screen_w - WINDOW_W), random.randint(0, 90)
    return random.randint(0, 90), random.randint(0, screen_h - WINDOW_H)


def create_note(root, x, y, text):
    window = tk.Toplevel(root)
    window.title("温馨提示")
    window.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")
    window.resizable(False, False)
    window.attributes("-topmost", True)
    try:
        window.attributes("-alpha", 0.96)
    except tk.TclError:
        pass

    bg = random.choice(BG_COLORS)
    fg = random.choice(TEXT_COLORS)
    label = tk.Label(
        window,
        text=text,
        bg=bg,
        fg=fg,
        font=("微软雅黑", 14, "bold"),
        wraplength=WINDOW_W - 22,
        padx=10,
        pady=8,
    )
    label.pack(fill="both", expand=True)
    window.lift()
    return window


def animate_window(root, window, start, target, step=0):
    total_steps = max(1, MOVE_DURATION_MS // FRAME_MS)
    progress = min(1, step / total_steps)
    eased = ease_out_cubic(progress)
    x = int(start[0] + (target[0] - start[0]) * eased)
    y = int(start[1] + (target[1] - start[1]) * eased)
    window.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")
    if progress < 1 and window.winfo_exists():
        root.after(FRAME_MS, animate_window, root, window, start, target, step + 1)
    else:
        window.geometry(f"{WINDOW_W}x{WINDOW_H}+{target[0]}+{target[1]}")


def show_center_title(root, screen_w, screen_h, windows):
    title_w = 420
    title_h = 88
    x = int((screen_w - title_w) / 2)
    y = int((screen_h - title_h) / 2)
    title = tk.Toplevel(root)
    title.title("心之所向")
    title.geometry(f"{title_w}x{title_h}+{x}+{y}")
    title.resizable(False, False)
    title.attributes("-topmost", True)
    try:
        title.attributes("-alpha", 0.94)
    except tk.TclError:
        pass
    tk.Label(
        title,
        text=TITLE_TEXT,
        bg="#ff4d8d",
        fg="white",
        font=("微软雅黑", 24, "bold"),
        padx=20,
        pady=18,
    ).pack(fill="both", expand=True)
    title.lift()
    windows.append(title)


def main():
    root = tk.Tk()
    root.withdraw()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    targets = generate_heart_points(POINT_COUNT, screen_w, screen_h)
    texts = make_text_pool(POINT_COUNT)
    windows = []

    def close_all(_event=None):
        for window in list(windows):
            if window.winfo_exists():
                window.destroy()
        root.destroy()

    root.bind_all("<Escape>", close_all)

    def spawn(index=0):
        if index >= POINT_COUNT:
            root.after(900, show_center_title, root, screen_w, screen_h, windows)
            root.after(FINAL_HOLD_MS, close_all)
            return
        target = targets[index]
        start = random_start_point(index, screen_w, screen_h)
        note = create_note(root, start[0], start[1], texts[index])
        windows.append(note)
        animate_window(root, note, start, target)
        root.after(POPUP_INTERVAL_MS, spawn, index + 1)

    spawn()
    root.mainloop()


if __name__ == "__main__":
    main()
