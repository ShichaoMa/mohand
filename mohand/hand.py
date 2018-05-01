import abc
import six
import click
import stevedore

from mohand.exception import HandDuplicationOfNameError
from mohand.utils import Singleton, _AttributeDict


@six.add_metaclass(abc.ABCMeta)
class HandBase(object):
    """
    用于定义hand任务的基类
    """
    @abc.abstractmethod
    def register(self, *args, **kwargs):
        """
        注册hand任务

        :return: 返回待注册的hand函数
        :rtype: function
        """


class HandDict(_AttributeDict):
    """
    Hand扩展插件集合字典(单例)
    """
    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['_click'] = click


def load_hands():
    """
    加载hand扩展插件

    :return: 返回hand注册字典(单例)
    :rtype: HandDict
    """
    handdict = HandDict()

    # 注册hand插件
    mgr = stevedore.ExtensionManager(
        namespace='mohand.plugin.hand',
        invoke_on_load=True)

    def register_hand(ext):
        _hand = ext.obj.register()
        if hasattr(handdict, _hand.__name__):
            raise HandDuplicationOfNameError(_hand.__name__)
        handdict[_hand.__name__] = _hand
        # print('register hand:', _hand.__name__)

    mgr.map(register_hand)
    # print('HandDict@mohand:', handdict)
    # print('HandDict@mohand:', id(handdict))

    return handdict
