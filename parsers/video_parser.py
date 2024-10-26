from moviepy.editor import VideoFileClip

# Загрузка видеофайла
clip = VideoFileClip("screen_captrue.webm")

# Сохранение как mp4
clip.write_videofile("output.mp4", codec="libx264")