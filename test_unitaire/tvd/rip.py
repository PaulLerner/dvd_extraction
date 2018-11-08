from xml.dom import minidom
import subprocess
import os

input_path = '/vol/work2/maurice/dvd'
output_path = '/vol/work3/maurice'
path_vobsub2srt = '/people/bredin/dev/VobSub2SRT/build/bin/vobsub2srt'

class Ripper(object):

    def lsdvd(self, name, season, first, last):
        with open(os.devnull, mode='w') as f:
            doc = subprocess.check_output([
            'lsdvd', '-x', '-Ox',
            f'{input_path}/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}'],
            stderr = f, timeout=5)
        doc = doc.decode('utf-8', 'ignore').replace('&', '')
        doc = doc.encode('utf-8')
        return doc

    def rip(self, episodes, name, season, first, last):
        i = first

        if not os.path.exists(f'{output_path}/{name}'):
            os.makedirs(f'{output_path}/{name}')

        with open(os.devnull, mode='w') as f:
            for e in episodes:
                subprocess.call([
                'HandBrakeCLI', '-i', f'{input_path}/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}', '-t', e.title, '-o',
                f'{output_path}/{name}/{name}.Season{int(season):02d}.Episode{i:02d}.mkv',
                '--cfr', '--crop', '0:0:0:0', '-r', '25', '--all-audio', '--all-subtitles'
                ])

                i += 1

    def rip_audio(self, audios, episodes, name, season, first):
        i = first

        with open(os.devnull, mode='w') as f:
            for e in episodes:
                for a in audios:
                    subprocess.call([

                    'ffmpeg',
                    '-i', f'{output_path}/{name}/{name}.Season{int(season):02d}.Episode{i:02d}.mkv',
                    '-map', '0:' + a.title, '-y',
                    f'{output_path}/{name}/{name}.Season{int(season):02d}.Episode{i:02d}.{a.langcode}48kHz.wav'])

                    subprocess.call([

                    'ffmpeg',
                    '-i', f'{output_path}/{name}/{name}.Season{int(season):02d}.Episode{i:02d}.mkv',
                    '-map', '0:' + a.title, '-y', '-ar', '16000', '-ac', '1',
                    f'{output_path}/{name}/{name}.Season{int(season):02d}.Episode{i:02d}.{a.langcode}16kHz.wav'])

                i += 1


    def rip_subtitles(self, subtitles, episodes, name, season, first, last):
        i = first

        with open(os.devnull, mode='w') as f:
            for e in episodes:
                for s in subtitles:
                    subprocess.call([
                    'mencoder', f'dvd://{e.title}', '-dvd-device',
                    f'{input_path}/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}',
                    '-o', '/dev/null', '-nosound', '-ovc', 'copy',
                    '-vobsubout', f'{output_path}/{name}/{name}.Season{int(season):02d}.Episode{i:02d}.{s.langcode}',
                    '-slang', s.langcode
                    ])

                    subprocess.call([path_vobsub2srt,
                    f'{output_path}/{name}/{name}.Season{int(season):02d}.Episode{i:02d}.{s.langcode}'
                    ])

                    subprocess.call([
                    'rm',
                    f'{output_path}/{name}/{name}.Season{int(season):02d}.Episode{i:02d}.{s.langcode}.sub'
                    ])

                    subprocess.call([
                    'rm',
                    f'{output_path}/{name}/{name}.Season{int(season):02d}.Episode{i:02d}.{s.langcode}.idx'
                    ])

                i += 1

    def get_contentTitle(self, content):
        return content.getElementsByTagName('title')[0].firstChild.data

    def get_tracks(self, content):
        track = content.getElementsByTagName('track')
        tracks = []

        for t in track:
            ix = t.getElementsByTagName('ix')[0]
            length = t.getElementsByTagName('length')[0]
            vts = t.getElementsByTagName('vts')[0]
            ttn = t.getElementsByTagName('ttn')[0]

            t = Track(ix.firstChild.data, length.firstChild.data, vts.firstChild.data, ttn.firstChild.data)
            tracks.append(t)

        return tracks

    def get_languages(self, content, first, last):
        audios = []
        languages = []

        tracks_content = content.getElementsByTagName('track')

        tracks   = self.get_tracks(content)
        tracks   = self.sort_tracks(tracks)
        episodes = self.get_episodes(tracks, first, last)
        episodes = self.sort_episodes(episodes)
        i = int(episodes[0].title)

        print(str(i))

        audio = tracks_content[i-1].getElementsByTagName('audio')

        for a in audio:
            title = a.getElementsByTagName('ix')[0]
            language = a.getElementsByTagName('language')[0]
            langcode = a.getElementsByTagName('langcode')[0]
            channels = a.getElementsByTagName('channels')[0]
            if title.firstChild and language.firstChild and langcode.firstChild and channels.firstChild:
                print(title.firstChild.data, language.firstChild.data, langcode.firstChild.data, channels.firstChild.data)
                audios.append(
                Audio(  title.firstChild.data,
                        language.firstChild.data,
                        langcode.firstChild.data,
                        channels.firstChild.data))

#        for a in audios:
#            for i in range(1,len(audios)):
#                if a.language == audios[i].language:
#                    if a.channels < audios[i].channels:
#                        audios.remove(audios[i])
#                    if a.channels > audios[i].channels:
#                        audios.remove(a)

        remove = []
        for i in range(0,len(audios)):
            for j in range(i+1, len(audios)):
                if audios[i].language == audios[j].language:
                    remove.append(j)

        remove = list(set(remove))
        remove = sorted(remove, reverse=True)
        print(remove)

        for r in remove:
            audios.remove(audios[r])

        return audios

    def get_subtitles(self, content, first, last):
        subtitles = []

        tracks_content = content.getElementsByTagName('track')

        tracks   = self.sort_tracks(self.get_tracks(content))
        episodes = self.sort_episodes(self.get_episodes(tracks, first, last))
        i = int(episodes[0].title)

        print(str(i))

        subtitle = tracks_content[i-1].getElementsByTagName('subp')

        for s in subtitle:
            title = s.getElementsByTagName('ix')[0]
            langcode = s.getElementsByTagName('langcode')[0]
            language = s.getElementsByTagName('language')[0]
            subtitles.append(Sub( title.firstChild.data,
                                  langcode.firstChild.data,
                                  language.firstChild.data ))

        remove = []

        for i in range(0,len(subtitles)):

            if subtitles[i].language == 'Unknown':
                remove.append(i)

            for j in range(i+1, len(subtitles)):
                if subtitles[i].language == subtitles[j].language:
                    remove.append(j)

        remove = list(set(remove))
        remove = sorted(remove, reverse=True)
        print(remove)

        for r in remove:
            subtitles.remove(subtitles[r])

        return subtitles


    def get_episodes(self, tracks, first, last):
        nbEpisodes = (last - first) + 1

        if nbEpisodes > 1 and tracks[0].duration > tracks[1].duration*1.5 :
            return tracks[1:nbEpisodes+1]
        else:
            return tracks[0:nbEpisodes]

    def sort_tracks(self, tracks):
        return sorted(tracks, key=lambda x: x.duration, reverse=True)

    def sort_episodes(self, episodes):
        return sorted(episodes, key=lambda x: x.title)

    def print_tracks(self, tracks):
        for t in tracks:
            print('Title ' + t.title + ' : ' + str(t.duration))
            print('vts', t.vts, 'ttn', t.ttn)

    def print_episodes(self, episodes):
        for i, e in enumerate(episodes):
            print('Episode ' + str(i+1) + ' : title -> ' + e.title + ' | duration -> ' + str(e.duration))

    def print_contentTitle(self, content):
        print('Content title : ' + self.get_contentTitle(content))

class Track:
    def __init__(self, ix, length, vts, ttn):
        self.title = str(ix)
        self.duration = float(length)
        self.vts = float(vts)
        self.ttn = float(ttn)

class Audio:
    def __init__(self, title, language, langcode, channels):
        self.title    = str(title)
        self.language = str(language)
        self.langcode = str(langcode)
        self.channels = int(channels)

class Sub:
    def __init__(self, title, langcode, language):
        self.title    = str(title)
        self.langcode = str(langcode)
        self.language = str(language)
