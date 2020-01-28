import os
import urllib

from wechatpy import create_reply
import wechatpy.messages as messages
from wechatpy.replies import ArticlesReply
from wechatpy.utils import ObjectDict
from youdao.spider import YoudaoSpider


emoji_list = ["/::)", "/::~", "/::B", "/::|", "/:8-)", "/::<", "/::$", "/::X", "/::Z", "/::'(", "/::-|", "/::@", "/::P", "/::D", "/::O", "/::(", "/:--b", "/::Q", "/::T", "/:,@P", "/:,@-D", "/::d", "/:,@o", "/:|-)", "/::!", "/::L", "/::>", "/::,@", "/:,@f", "/::-S", "/:?", "/:,@x", "/:,@@", "/:,@!", "/:!!!", "/:xx", "[Bye]", "/:wipe", "/:dig", "/:handclap", "/:B-)", "/:<@", "/:@>", "/::-O", "/:>-|", "/:P-(", "/::'|", "/:X-)", "/::*", "/:8*", "/:pd", "/:<W>", "/:beer", "/:coffee", "/:pig", "/:rose", "/:fade", "/:showlove", "/:heart", "/:break", "/:cake", "/:bome", "/:shit", "/:moon", "/:sun", "/:hug", "/:strong", "/:weak", "/:share", "/:v", "[Salute]", "/:jj", "/:@@", "/:ok", "/:jump", "/:shake", "/:<O>", "/:circle", "😄", "😷", "😂", "😝", "😳", "😱", "😔", "😒", "[Hey]", "[Facepalm]", "[Smirk]", "[Smart]", "[Concerned]", "[Yeah!]", "[Onlooker]", "[GoForIt]", "[Sweats]", "[OMG]", "[Emm]", "[Respect]", "[Doge]", "[NoProb]", "[MyBad]", "[Wow]", "👻", "🙏", "💪", "🎉", "🎁", "[Packet]", "[Rich]", "[Blessing]"]

def create_text_from_result(result):
    text = ''
    if result['errorCode'] != 0:
        text += YoudaoSpider.error_code[result['errorCode']]
    else:
        text += (result['query'] + '\n')
        if 'basic' in result:
            if 'us-phonetic' in result['basic']:
                text += '{} {}\n'.format(u'美音:', '[%s]' % result['basic']['us-phonetic'])
            if 'uk-phonetic' in result['basic']:
                text += '{} {}\n'.format(u'英音:', '[%s]' % result['basic']['uk-phonetic'])
            if 'phonetic' in result['basic']:
                text += '{} {}\n'.format(u'拼音:', '[%s]' % result['basic']['phonetic'])

            text += u'基本词典:\n'
            text += '\t'+'\n\t'.join(result['basic']['explains']) + '\n'

        if 'translation' in result:
            text += u'有道翻译:\n'
            text += '\t'+'\n\t'.join(result['translation']) + '\n'

        if 'web' in result:
            text += u'网络释义:\n'
            for item in result['web']:
                text += ('\t' + item['key'] + ': ' + '; '.join(item['value']) + '\n')
    return text

def msg_handler(msg):
    if msg.type == 'text':
        content = msg.content
        print(content)
        # fight with emoji!
        has_emoji = False
        for e in emoji_list:
            if e in content:
                has_emoji = True
                content = content.replace(e, '[Smirk]')
        if has_emoji:
            return create_reply(content, msg)
        spider = YoudaoSpider(content)
        result = spider.get_result(use_api=True)
        text = create_text_from_result(result)
    elif msg.type == 'event' and msg.event == 'subscribe':
        text = '欢迎来到清微小译!\n\n'
        text += '只需要回复想要翻译的中文或英文单词,即可查看翻译结果~\n'
    else:
        text = '暂不支持该数据类型.'
    reply = create_reply(text, msg)
    return reply
