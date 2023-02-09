import os
files = os.listdir("top-followers")
all = set()
out = []
for file in files:
	with open("top-followers/"+file, "r") as f:
		links = f.read().split('\n')
		for l in links:
			if len(l) > 0:
				if l not in all:
					all.add(l)
					out.append(l)
print(all)
with open("top-followers.txt", "w") as f:
	f.write('\n'.join(list(out)))
