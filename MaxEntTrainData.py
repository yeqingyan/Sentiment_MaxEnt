import re
import sys
import emoji
import argparse
from Pipeline import Pipeline

class MaxEntTrainData(Pipeline):
    def process(self):
        # Count sentiment result: Neg(-1), Neu(0), Pos(1)
        result_count = {
            -1: 0, 0:0, 1:0,
            "emoji": 0,
            "emoticon": 0}

        emoticon_re = self.emoticon_init()
        emoji_re = self.emoji_init()
        for line in self.input.readlines():
            emoji_label, emoticon_label = self.get_labels(line.strip(), emoticon_re, emoji_re)
            if emoji_label == emoticon_label == -2:
                continue
            self.write_train_set(line, emoji_label, emoticon_label, result_count, self.output)

    def get_labels(self, text, emoticon_re, emoji_re):
        """ Get emoji/emoticon labels """

        # -2 means text do not have emojis/emoticons
        emoticon_label = -2
        emoji_label = -2

        # Check if text contain emoticon
        match_str = re.findall(emoticon_re["emoticon"], text)
        if match_str:
            emoticon_label = self.emoticon_analysis(text, emoticon_re)

        # Check if text contain emoji
        match_str = re.findall(emoji_re["emoji"], text)
        if match_str:
            emoji_label = self.emoji_analysis(match_str, emoji_re)
        return emoji_label, emoticon_label

    def emoji_init(self):
        """ Generate emoji regular expression """
        # Postive
        positive_emojis = [
            ':smile:',
            ':laughing:',
            ':blush:',
            ':smiley:',
            ':relaxed:',
            ':smirk:',
            ':heart_eyes:',
            ':kissing_heart:',
            ':kissing_closed_eyes:',
            ':satisfied:',
            ':grin:',
            ':wink:',
            ':stuck_out_tongue_winking_eye:',
            ':stuck_out_tongue_closed_eyes:',
            ':grinning:',
            ':kissing:',
            ':kissing_smiling_eyes:',
            ':stuck_out_tongue:',
            ':sweat_smile:',
            ':innocent:',
            ':heart:',
            ':relieved:',
            ':open_mouth:',
            ':grimacing:',
            ':smiling_imp:',
            ':scream:',
            ':smiling_imp:'
        ]

        # Neutral
        neutral_emojis = [
            ':face_with_cold_sweat:',
            ':worried:',
            ':crying_face:',
            ':anguished:',
            ':sleepy:',
            ':sob:',
            ':hushed_face:',
            ':cold_sweat:',
            ':astonished_face:',
            ':flushed:',
            ':sleeping:',
            ':dizzy_face:',
            ':broken_heart:',
            ':no_mouth:',
            ':disappointed_relieved:',
            ':fearful:'
        ]

        # Negative
        negative_emojis = [
            ':imp:',
            ':neutral_face:',
            ':expressionless:',
            ':unamused:',
            ':pensive:',
            ':confused:',
            ':confounded:',
            ':disappointed:',
            ':angry:',
            ':rage:',
            ':persevere:',
            ':triumph:',
            ':frowning:',
            ':weary:',
            ':tired_face:',
            ':mask:'
        ]

        positive_emojis = set([emoji.emojize(moji, use_aliases=True) for moji in positive_emojis])
        neutral_emojis = set([emoji.emojize(moji, use_aliases=True) for moji in neutral_emojis])
        negative_emojis = set([emoji.emojize(moji, use_aliases=True) for moji in negative_emojis])
        emoji_list = list(positive_emojis) + list(neutral_emojis) + list(negative_emojis)

        # Create regular expression match
        emoji_re_str = r"|".join(emoji_list)
        emoji_re = re.compile(r"(" + emoji_re_str + r")")
        return {
            "emoji": emoji_re,
            "pos_emoji": positive_emojis,
            "neu_emoji": neutral_emojis,
            "neg_emoji": negative_emojis
        }

    def emoticon_init(self):
        """
        Generate emoticon regular expression
        This part of code was modified from https://github.com/brendano/tweetmotif
        """
        mycompile = lambda pat:  re.compile(pat,  re.UNICODE)

        NormalEyes = r'[:=]'
        Wink = r'[;]'
        NoseArea = r'(|o|O|-)'   ## rather tight precision, \S might be reasonable...
        HappyMouths = r'[D\)\]]'
        SadMouths = r'[\(\[]'
        Tongue = r'[pP]'
        OtherMouths = r'[doO\\]'  # remove forward slash if http://'s aren't cleaned
        Happy_RE =  mycompile( '(\^_\^|' + '(' + NormalEyes + '|' + Wink + ")"+ NoseArea + '(' + HappyMouths + '|' + Tongue + ')' + ')')
        Sad_RE = mycompile(NormalEyes + NoseArea + SadMouths)
        Normal_RE = mycompile(NormalEyes + NoseArea + OtherMouths)
        Emoticon = (
            "("+NormalEyes+"|"+Wink+")" +
            NoseArea +
            "("+Tongue+"|"+OtherMouths+"|"+SadMouths+"|"+HappyMouths+")"
        )
        Emoticon_RE = mycompile(Emoticon)
        return { "emoticon":            Emoticon_RE,
                "happy_emoticon":      Happy_RE,
                "normal_emoticon":     Normal_RE,
                "sad_emoticon":        Sad_RE}

    def emoji_analysis(self, match_str, emoji_re):
        """ Return text's emoji sentiment result """
        emoji_count = [0,0,0]
        for match_moji in match_str:
            if match_moji in emoji_re["pos_emoji"]:
                emoji_count[2] += 1
            if match_moji in emoji_re["neu_emoji"]:
                emoji_count[1] += 1
            if match_moji in emoji_re["neg_emoji"]:
                emoji_count[0] += 1
        if emoji_count.count(0) != 2:
            # Discard text if it contain more than 1 polarity
            return -2
        elif emoji_count[0] > 0:
            # Negative tweets
            return -1
        elif emoji_count[2] > 0:
            # Positive tweets
            return 1
        elif emoji_count[1] > 0:
            # Neutrial tweets
            return 0

    def emoticon_analysis(self, text, emoticon_re):
        """ Return text's emoticon sentiment result """
        h= emoticon_re["happy_emoticon"].search(text)
        s= emoticon_re["sad_emoticon"].search(text)
        n= emoticon_re["normal_emoticon"].search(text)
        # Discard text if it contain more than 1 polarity
        if [h, s, n].count(None) != 2:
            return -2
        if h: return 1
        if s: return -1
        if n: return 0
        return -2

    def write_train_set(self, text, emoji_label, emoticon_label, result_count, train_file):
        """ Write train dataset to train_file """

        # Text contain both emoji and emoticon
        if emoticon_label != -2 and emoji_label != -2:
            if emoticon_label != emoji_label:
                # discard if emoji&emoticon do not match
                return
            else:
                # Emoticon and emoji agree with each other
                train_file.write("{0}\t{1}".format(emoticon_label, text))
                result_count[emoticon_label] += 1
                result_count["emoji"] += 1
                result_count["emoticon"] += 1
        # text contin emoticon only
        elif emoticon_label != -2:
            train_file.write("{0}\t{1}".format(emoticon_label, text))
            result_count[emoticon_label] += 1
            result_count["emoticon"] += 1
        # text contin emoji only
        elif emoji_label != -2:
            train_file.write("{0}\t{1}".format(emoji_label, text))
            result_count[emoji_label] += 1
            result_count["emoji"] += 1
        else:
            print("ERROR: Compare emoticon and emoji")
            return