import sys
import time

def progress_bar(total):
    bar_length = 50
    for i in range(total + 1):
        progress = i / total
        bar = '[' + '#' * int(progress * bar_length) + ' ' * (bar_length - int(progress * bar_length)) + ']'
        sys.stdout.write('\rЗагрузка: {}% {}'.format(int(progress * 100), bar))
        sys.stdout.flush()
        time.sleep(0.1)  # Эмулируем процесс загрузки
    print('\nЗагрузка завершена.')