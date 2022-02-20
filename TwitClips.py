#!/usr/bin/python3

import urllib3, requests, sys, signal, argparse, re, os
from colorama import init, Fore

init(autoreset=True)
clipr_xyz_url = "https://clipr.xyz/"
#Colors
blue, red, green, lgcyan = Fore.BLUE, Fore.RED, Fore.GREEN, Fore.LIGHTCYAN_EX
status = f"{Fore.YELLOW}[{Fore.LIGHTMAGENTA_EX}*{Fore.YELLOW}]{blue}"
good_status = f"{Fore.LIGHTBLUE_EX}[{Fore.LIGHTGREEN_EX}+{Fore.LIGHTBLUE_EX}]{blue}"
urllib3.disable_warnings()

def banner():
	with open("banner", "r") as f:
		print(blue + f.read())
		f.close()

def getArgs():
	banner()
	parser = argparse.ArgumentParser()
	group1 = parser.add_mutually_exclusive_group(required=True)
	group1.add_argument("-f", "--file", help="File with clips to download", default=False)
	group1.add_argument("-c", "--clip", help="Clip to download", default=False)
	parser.add_argument("-p", "--path", help="Path where all downloaded clips will be stored", required=True)
	parser.add_argument("-r", "--resolution", help="Resolution that the downloaded clip will have, by default: 1080p", default="1080", choices=["1080", "720", "480", "360"])
	args = parser.parse_args()
	return args.file, args.clip, args.path, args.resolution

def capture1080p(text):
	return re.findall(r'<span>1080p<\/span>\n(?:.+\n)+.*[^-0-9]\.mp4">\n<span>Download<\/span>', text)[0]

def capture720p(text):
	return re.findall(r'<span>720p<\/span>\n(?:.+\n)+.*720\.mp4">\n<span>Download<\/span>', text)[0]

def capture480p(text):
	return re.findall(r'<span>480p<\/span>\n(?:.+\n)+.*480\.mp4">\n<span>Download<\/span>', text)[0]

def capture360p(text):
	return re.findall(r'<span>360p<\/span>\n(?:.+\n)+.*360\.mp4">\n<span>Download<\/span>', text)[0]

def checkResolution(resolution, resolutionContent):

	if resolution == "1080":
		return capture1080p(resolutionContent)

	elif resolution == "720":
		return capture720p(resolutionContent)

	elif resolution == "480":
		return capture480p(resolutionContent)

	elif resolution == "360":
		return capture360p(resolutionContent)

# Gets the link of the clip to be downloaded
def getClipDownloadLink(resolLink):
	clip2download = re.findall(r'(https:\/\/.*.mp4)"', resolLink)[0]
	return clip2download

# Send a request to the "url" with the clip to be downloaded
def ask4clip(url, resolution):
	global s
	s = requests.session()
	r = s.get(clipr_xyz_url)
	r = s.get(url)
	resolLink = checkResolution(resolution, r.text)
	return resolLink

# Gets the clip identifier, example: OutstandingTriumphantTubersAsianGlow-XDV9sQ1F89eD24de
def parseClipUrl(clip_url):
	id_clip_url = re.findall(r'https:\/\/.*\/(.*)$', clip_url)[0]

	# If the url has a "?" remove it
	if "?" in id_clip_url:
		id_clip_url = re.findall(r'(.*)\?', id_clip_url)[0]
	return id_clip_url

# Download The clip and save it with the "id_clip_url" as name
def download(clip2download, id_clip_url, clip_path):
	r = s.get(clip2download)
	final_path = os.path.join(clip_path, id_clip_url + ".mp4")
	with open(final_path, "wb") as f:
		print(f"\t{blue}{good_status} {Fore.YELLOW}Saving on: {lgcyan}{final_path}\n")
		f.write(r.content)
		f.close()

# Single clip download Function
def oneClip(clip_url, clip_resolution, clip_path):
	id_clip_url = parseClipUrl(clip_url)

	print(f"{blue}{status} Getting the {lgcyan}urls{blue} to download the {lgcyan}clips")
	resolLink = ask4clip(clipr_xyz_url + id_clip_url, clip_resolution)
	clip2download = getClipDownloadLink(resolLink)

	print(f"{blue}{status} Downloading: {lgcyan}{clip2download}")
	download(clip2download, id_clip_url, clip_path)

# Function to download a list of clips from a file
def moreTOne(clip_resolution, clip_path, clips_file):
	all_clips = readClipsFile(clips_file).split()
	clip2download_arr = dict()

	print(f"{blue}{status} Getting the {lgcyan}urls{blue} to download the {lgcyan}clips")
	for clip in all_clips:
		id_clip_url = parseClipUrl(clip)
		clip2download = getClipDownloadLink(ask4clip(clipr_xyz_url + id_clip_url, clip_resolution))
		clip2download_arr.update({id_clip_url : clip2download})

	for id_clip_url, clip2download in clip2download_arr.items():
		print(f"{blue}{status} Downloading: {lgcyan}{clip2download}")
		download(clip2download, id_clip_url, clip_path)

def readClipsFile(clips_file):
	with open(clips_file, "r") as f:
		clips = f.read()
		f.close()
	return clips

def checkPath(path):
	if not os.path.isdir(path):
		print(f"{red}[!]{blue} The path: {lgcyan}{path}{blue} does {lgcyan}not exist")
		sys.exit()

# Main Function
def main():
	clips_file, clip_url, clip_path, clip_resolution = getArgs()
	checkPath(clip_path)
	if clip_url:
		oneClip(clip_url, clip_resolution, clip_path)
	elif clips_file:
		moreTOne(clip_resolution, clip_path, clips_file)

def sig_handler(signum, frame):
	print(f"\n{red}[!]{blue} Exiting...\n")
	sys.exit()

signal.signal(signal.SIGINT, sig_handler)

if __name__ == '__main__':
	main()
