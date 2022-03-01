import tqdm, time

with tqdm.tqdm(total=100) as pbar:
    for i in range(110):
        # pbar.update(i)
        pbar.update(1)
        time.sleep(0.05)
