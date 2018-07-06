from xml.dom import minidom
import subprocess 
import os 
import errno

class Ripper(object):

    ''' Process the lsdvd command and return the file '''
        
    def lsdvd(self):
        with open(os.devnull, mode='w') as f:
            doc = subprocess.check_output(
            ['lsdvd', '-x', '-Ox', '/dev/dvd'], stderr = f, timeout=5)
        return doc 
        
    ''' Encode and recode the file to make sure there is no encoding problem  '''
    
    def recode(self, doc):
        doc = doc.decode('utf-8', 'ignore').replace('&', '')
        doc = doc.encode('utf-8')
        return doc
    
    ''' Create the .mkv file of each episode '''    
        
    def rip(self, episodes, name, season, first):

        i = first
        
        if not os.path.exists(name):
            os.makedirs(name)
        if not os.path.exists(name + '/' + season):
            os.makedirs(name + '/' +season)
        
        with open(os.devnull, mode='w') as f:
            for e in episodes:    
                subprocess.call(
                ['HandBrakeCLI', '-i', '/dev/dvd', '-t', '1', '-o', 
                name + '/' + season + '/' +
                name + '.Season' + season + '.Episode' + '0' + str(i) +'.mkv',
                '--cfr', '-r', '25', '--all-audio', '--all-subtitles'])
                i += 1
       
    ''' Return the title written in the file '''
    
    def get_contentTitle(self, content):
        contentTitle = content.getElementsByTagName('title')[0].firstChild.data
        return contentTitle
        
    ''' Return the list of the tracks in the file with their title and duration '''
        
    def get_tracks(self, content):
        track = content.getElementsByTagName('track')
        tracks = []

        i = 0

        for t in track:
            ix = t.getElementsByTagName('ix')[0]
            length = t.getElementsByTagName('length')[0]
            
            t = Track(ix.firstChild.data, length.firstChild.data)
            tracks.append(t)
        return tracks
        
    ''' Return the list of languages of the content '''
    
    def get_languages(self, content):
        
        audios = []
        languages = []    
        
        tracks = content.getElementsByTagName('track')
        for t in tracks:
            audio = t.getElementsByTagName('audio')
        for a in audio:
            lang = a.getElementsByTagName('language')[0]
            chan = a.getElementsByTagName('channels')[0]
            audios.append(Audio(lang.firstChild.data, chan.firstChild.data))

        return audios
   
    ''' Return the list of real episodes from the tracks list '''    

    def get_episodes(self, tracks, first, last):
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
            for i in range(0,nbEpisodes+0):
                episodes.append(tracks[i])
        return episodes     
        
    ''' Return the tracks list sorted by their duration (top-down) '''    
        
    def sort_tracks(self, tracks):
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
        
    '''
    def get_duree(Piste):
        return Piste.duree
        
    sorted(pistes, key=pistes.get_duree, reverse=True)
    '''

    '''  '''

    def sort_episodes(self, episodes):
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

    ''' Display the tracks '''
                
    def print_tracks(self, tracks):
        for t in tracks:
            print('Title ' + t.title + ' : ' + str(t.duration))              

    ''' Display the episodes '''
            
    def print_episodes(self, episodes):
        i = 1
        for e in episodes:
            print('Episode ' + str(i) + ' : title -> ' + e.title + ' | duration -> ' + str(e.duration))
            i += 1
            
    ''' Display the content title '''
    def print_contentTitle(self, content):
        print('Content title : ' + self.get_contentTitle(content))
    


class Track:
    def __init__(self, ix, length):
        self.title = str(ix)
        self.duration = float(length)  
        

class Audio:
    def __init__(self, language, channels):
        self.language = str(language)
        self.channels = int(channels)


    



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
