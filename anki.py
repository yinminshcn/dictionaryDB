import genanki

model_id = 'EEWLT'
deck_id = 'MinYin'

def createId(name):
    sum = 0
    for c in name:
        sum = sum * 100 + ord(c)
        pass
    return sum

if __name__ == "__main__":
    script = '''
  <script>
  		function play(audio){
			return new Promise((res, rej) => {
				audio.addEventListener('ended', ()=>{
					setTimeout(() => res(), 1000);
				});
				audio.play();
			});
		}
		async function playAllAudio(){
			var audios = $("audio").toArray();
			for(var k = 0; k < audios.length; k++){
				await play(audios[k]);
			}
		}

		onPageFinished = (function(_super) {
			return function(){
				_super.apply(this, arguments);
				playAllAudio();
			};
		})(onPageFinished);
  </script>
    '''

    my_model = genanki.Model(
        createId(model_id),
        'Extend English Word List',
        fields=[
            {
                "name": "Word"
            },
            {
                "name": "Image",
            },
            {
                "name": "Sound",
            },
            {
                "name": "Sound_Meaning",
            },
            {
                "name": "Sound_Example",
            },
            {
                "name": "Meaning",
            },
            {
                "name": "Example",
            },
            {
                "name": "IPA",
            },
            {
                "name": "Chinese",
            },
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': script + '''
           <div style='font-family: Arial; color:#FF80DD;'>{{Word}}</div>
           
           {{#Image}}
           <hr>
               <img  alt="url data scheme" {{Image}} />
           {{/Image}}
           
           {{#Meaning}}
           <hr>
           <div style='font-family: Arial; color:#00aaaa; text-align:left;'>
                Meaning: {{Meaning}}
           </div>
           {{/Meaning}}
           
           {{#Chinese}}
           <hr>
           <div style='font-family: Arial; color:#00aaaa; text-align:left;'>
                Meaning: {{Chinese}}
           </div>
           {{/Chinese}}
           
           <hr>
           <div style='font-family: Arial; color:#9CFFFA; text-align:left;'>
               &nbsp;→&nbsp;Example: {{Example}}
           </div>
           <hr>
           
           {{#Sound_Meaning}}
           <audio {{Sound_Meaning}}></audio>
           {{/Sound_Meaning}}
           
           {{#Sound_Example}}
           <audio {{Sound_Example}}></audio>
           {{/Sound_Example}}
      ''',
                'afmt': script + '''
           <div id='rubric'>20000 Essential English Words</div>
           <div style='font-family: Arial; font-size: 70px;color:#FF80DD;'>{{Word}}</div>
           <hr>
           <div style='font-family: Arial; font-size: 70px;color:#FF80DD;'>{{IPA}}</div>
           <audio {{Sound}}> </audio>
      ''',
            },
        ],
        css='''
        .card {
             font-family: arial;
             font-size:150%;
             text-align: center;
             color: Black;
             background-color:black;
        }
        #rubric {
             text-align: left;
             padding: 4px;
             padding-left: 10px;
             padding-right: 10px;
             margin-bottom: 10px;
             background: #1d6695;
             color: white;
             font-weight: 500;
        }
        img{
             max-width:100%;
             height:auto;
             width:300px;
             border-radius: 20px;
        }
  '''
    )

    import fetch

    my_note = genanki.Note(
        model=my_model,
        fields=[
            'run',
            fetch.fetch('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Flickr_cc_runner_wisconsin_u.jpg/220px-Flickr_cc_runner_wisconsin_u.jpg'),
            fetch.fetch('https://upload.wikimedia.org/wikipedia/commons/a/a9/En-us-run.ogg'),
            fetch.fetch('https://dictionary.blob.core.chinacloudapi.cn/media/audio/tom/a4/b1/A4B16D8315BE09F7AD23C1824DB4B1B4.mp3'),
            fetch.fetch('https://dictionary.blob.core.chinacloudapi.cn/media/audio/tom/be/b6/BEB6373331B59DE147135452C2232800.mp3'),
            'To move swiftly',
            'Mornings begin with the smell of my "get up and go fast" brew in the kitchen before I fly out the door on my way to a run or the gym.',
            '/ɹʌn/',
            '跑'
        ])

    my_deck = genanki.Deck(
        createId(deck_id),
        'English Word Voculabary')

    my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file('output.apkg')
