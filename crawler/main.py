import blogsscraper as bs
import textscraper as ts
import time


def main():
    # bs.get_profiles(100)
    bs.get_blog()
    ts.get_text()
    print("s1")


if __name__ == '__main__':
    start_time = time.time()
    main()
    print('\n--- %s seconds ---' % (time.time() - start_time))
