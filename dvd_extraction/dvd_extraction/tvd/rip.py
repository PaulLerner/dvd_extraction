from xml.dom import minidom
import subprocess
import os

path = '/vol/work2/maurice/'

class Ripper(object):

    def lsdvd(self, name, season, first, last):
        """

        Process the lsdvd command and return the file

        Parameters
        ----------
        name : str
            Name of the serie.
        season : str
            The number of the season.
        first, last : int
            The number of the first and the last episode on the disk.

        Returns
        -------
        doc : bytes
            content of the lsdvd command.

        """

        with open(os.devnull, mode='w') as f:
            doc = subprocess.check_output([
            'lsdvd', '-x', '-Ox',
            f'{path}dvd/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}'],
            stderr = f, timeout=5)
        return doc

    def recode(self, doc):
        """

        Recode the doc into utf-8 without unsupported symbols

        Parameters
        ----------
        doc : bytes
            doc you need to recode.

        Returns
        -------
        doc : bytes
            content of the recode doc.

        """

        doc = doc.decode('utf-8', 'ignore').replace('&', '')
        doc = doc.encode('utf-8')

        return doc

    def rip(self, episodes, name, season, first, last):
        """

        Create the .mkv file of each episode

        Parameters
        ----------
        episodes : list
            List of the episodes to rip.
        name : str
            Name of the serie.
        season : str
            The number of the season.
        first, last : int
            The number of the first and the last episode on the disk.

        """

        i = first
        int(season)

        if not os.path.exists(f'{name}'):
            os.makedirs(f'{name}')
        if not os.path.exists(f'{name}/{int(season):02d}'):
            os.makedirs(f'{name}/{int(season):02d}')

        with open(os.devnull, mode='w') as f:
            for e in episodes:
                subprocess.call([

                'HandBrakeCLI', '-i', f'{path}dvd/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}', '-t', e.title, '-o',
                f'{name}/{int(season):02d}/{name}.Season{int(season):02d}.Episode{i:02d}.mkv',
                '--cfr', '-r', '25', '--all-audio', '--all-subtitles'

                ])

                i += 1

    def rip_audio(self, audios, episodes, name, season, first):
        """

        Create the .wav file of each episode and language in 16kHz and 48kHz

        Parameters
        ----------
        audios : list
            List of the languages to extract.
        episodes : list
            List of the episodes we want to extract audio.
        name : str
            Name of the serie.
        season : str
            The number of the season.
        first, last : int
            The number of the first and the last episode on the disk.

        """

        i = first

        with open(os.devnull, mode='w') as f:
            for e in episodes:
                for a in audios:
                    subprocess.call([

                    'ffmpeg',
                    '-i', f'{name}/{int(season):02d}/{name}.Season{int(season):02d}.Episode{i:02d}.mkv',
                    '-map', '0:' + a.title, '-y',
                    f'{name}/{int(season):02d}/{name}.Season{int(season):02d}.Episode{i:02d}.{a.langcode}48kHz.wav'])

                    subprocess.call([

                    'ffmpeg',
                    '-i', f'{name}/{int(season):02d}/{name}.Season{int(season):02d}.Episode{i:02d}.mkv',
                    '-map', '0:' + a.title, '-y', '-ar', '16000', '-ac', '1',
                    f'{name}/{int(season):02d}/{name}.Season{int(season):02d}.Episode{i:02d}.{a.langcode}16kHz.wav'])

                i += 1


    def rip_subtitles(self, subtitles, episodes, name, season, first, last):
        """

        Create the .srt file of each episode and subtitle language

        Parameters
        ----------
        subtitles : list
            List of the subtitles to extract.
        episodes : list
            List of the episodes we want to extract audio.
        name : str
            Name of the serie.
        season : str
            The number of the season.
        first, last : int
            The number of the first and the last episode on the disk.

        """

        i = first

        with open(os.devnull, mode='w') as f:
            for e in episodes:
                for s in subtitles:
                    subprocess.call([

                    'mencoder', f'dvd://{e.title}', '-dvd-device',
                    f'{path}dvd/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}',
                    '-o', '/dev/null', '-nosound', '-ovc', 'copy',
                    '-vobsubout', f'{name}/{int(season):02d}/{name}.Season{int(season):02d}.Episode{i:02d}.{s.langcode}',
                    '-slang', s.langcode

                    ])

                    subprocess.call([

                    '/people/bredin/dev/VobSub2SRT/build/bin/vobsub2srt',
                    f'{name}/{int(season):02d}/{name}.Season{int(season):02d}.Episode{i:02d}.{s.langcode}'

                    ])

                    subprocess.call([
                    'rm',
                    f'{name}/{int(season):02d}/{name}.Season{int(season):02d}.Episode{i:02d}.{s.langcode}.sub'
                    ])

                    subprocess.call([
                    'rm',
                    f'{name}/{int(season):02d}/{name}.Season{int(season):02d}.Episode{i:02d}.{s.langcode}.idx'
                    ])

                i += 1

    def get_contentTitle(self, content):
        """

        Return the .xml title written in the file

        Parameters
        ----------
        content : bytes
            content you need to parse.

        Returns
        -------
        contentTitle : str
            title of the .xml file.

        """

        contentTitle = content.getElementsByTagName('title')[0].firstChild.data

        return contentTitle

    def get_tracks(self, content):
        """

        Return the list of the tracks in the .xml file with their title and duration

        Parameters
        ----------
        content : bytes
            content you need to parse.

        Returns
        -------
        tracks : list
            list of the tracks in the .xml file

        """

        track = content.getElementsByTagName('track')
        tracks = []

        i = 0

        for t in track:
            ix = t.getElementsByTagName('ix')[0]
            length = t.getElementsByTagName('length')[0]

            t = Track(ix.firstChild.data, length.firstChild.data)
            tracks.append(t)

        return tracks

    def get_languages(self, content, first, last):
        """

        Return the list of languages in the .xml file with their title, language and langcode

        Parameters
        ----------
        content : bytes
            content you need to parse.
        first, last : int
            The number of the first and the last episode on the disk.

        Returns
        -------
        audios : list
            list of the languages in the .xml file

        """

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

        for a in audios:
            for i in range(1,len(audios)):
                if a.language == audios[i].language:
                    if a.channels < audios[i].channels:
                        audios.remove(audios[i])
                    if a.channels > audios[i].channels:
                        audios.remove(a)

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
        """

        Return the list of subtitles in the .xml file with their title, language and langcode

        Parameters
        ----------
        content : bytes
            content you need to parse.
        first, last : int
            The number of the first and the last episode on the disk.

        Returns
        -------
        subtitles : list
            list of the subtitles in the .xml file

        """

        subtitles = []

        tracks_content = content.getElementsByTagName('track')

        tracks   = self.get_tracks(content)
        tracks   = self.sort_tracks(tracks)
        episodes = self.get_episodes(tracks, first, last)
        episodes = self.sort_episodes(episodes)
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
        """

        Return the list of real episodes from the tracks list

        Parameters
        ----------
        tracks : list
            list of the video tracks in the .xml file
        first, last : int
            The number of the first and the last episode on the disk.

        Returns
        -------
        episodes : list
            list of the episodes in the .xml file

        """

        episodes = []
        nbEpisodes = (last - first) + 1

        if nbEpisodes > 1 and tracks[0].duration > tracks[1].duration*1.5 :
            firstTitleContainsAll = True
        else:
            firstTitleContainsAll = False

        if firstTitleContainsAll:
            for i in range(1,nbEpisodes+1):
                episodes.append(tracks[i])
        else:
            for i in range(0,nbEpisodes):
                episodes.append(tracks[i])

        return episodes

    def sort_tracks(self, tracks):
        """

        Return the tracks list sorted by their duration (top-down)

        Parameters
        ----------
        tracks : list
            list of the video tracks in the .xml file

        Returns
        -------
        tracks : list
            list of the sorted video tracks in the .xml file

        """

        swap = True
        i = 0
        while swap == True:
            swap = False
            i = i + 1
            for j in range(0, len(tracks)-i):
                if tracks[j].duration < tracks[j+1].duration:
                    swap = True
                    tracks[j],tracks[j+1] = tracks[j+1],tracks[j]

        return tracks

    def sort_episodes(self, episodes):
        """

        Return the episodes list sorted by supposed chronological order

        Parameters
        ----------
        episodes : list
            list of the episodes in the .xml file

        Returns
        -------
        episodes : list
            list of the sorted episodes in the .xml file

        """

        swap = True
        i = 0
        while swap == True:
            swap = False
            i = i + 1
            for j in range(0, len(episodes)-i):
                if int(episodes[j].title) > int(episodes[j+1].title):
                    swap = True
                    episodes[j],episodes[j+1] = episodes[j+1],episodes[j]

        return episodes

    def print_tracks(self, tracks):
        """

        Display the tracks in the .xml file

        Parameters
        ----------
        tracks : list
            list of the video tracks in the .xml file

        """

        for t in tracks:
            print('Title ' + t.title + ' : ' + str(t.duration))

    def print_episodes(self, episodes):
        """

        Display the episodes in the .xml file

        Parameters
        ----------
        episodes : list
            list of the episodes in the .xml file

        """

        i = 1
        for e in episodes:
            print('Episode ' + str(i) + ' : title -> ' + e.title + ' | duration -> ' + str(e.duration))
            i += 1

    def print_contentTitle(self, content):
        """

        Display the content title of the .xml file

        Parameters
        ----------
        content : bytes
            content of the .xml file.

        """

        print('Content title : ' + self.get_contentTitle(content))



class Track:
    def __init__(self, ix, length):
        self.title = str(ix)
        self.duration = float(length)


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




