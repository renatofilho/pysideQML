from PySide.QtCore import QUrl
from PySide.QtDeclarative import QDeclarativeComponent, QDeclarativeEngine

parent = 'parent'

class QMLProperty(object):
    _value = None
    _name = None
    _obj = None

    def __init__(self, obj, name = '', value = None):
        self._obj = obj
        self._name = name
        if isinstance(value, QMLProperty):
            self._value = value._value
        else:
            self._value = value
        self.update()

    def __set__(self, instance, value):
        self._value = value
        self.updatE()

    def __get__(self, instance, owner):
        return self._value

    def update(self):
        print "Set property", self._name, self._value
        self._obj.setProperty(self._name, self._value)

class Anchor(object):
    __fiels__   = ['baseline', 'baselineOffset',
                   'bottom', 'bottomOffset',
                   'centerIn',
                   'fill',
                   'horizontalCenter', 'horizontalCenterOffset',
                   'left', 'leftMargins',
                   'margins',
                   'mirrored',
                   'right', 'rightMargin',
                   'top', 'topMargin',
                   'verticalCenter', 'verticalCenterOffset']

    def __init__(self, **kargs):
        for key in kargs:
            setattr(self, key, kargs[key])

    """
    def createLayout(self, qmlObject):
        result = ''
        for field in self.__fiels__:
            try:
                attr = getattr(self, field)
                if attr:
                    result += 'anchors.%s: %s;' % (field, str(attr))
            except:
                pass
        return result
    """

class QMLItem(object):
    __engine__      = None
    __className__   = 'Item'
    __signals__     = {}

    def __init__(self, parentItem, **kargs):
        global parent
        parent = self

        if not QMLItem.__engine__:
            QMLItem.__engine__ = QDeclarativeEngine()
        component = QDeclarativeComponent(QMLItem.__engine__)
        qmlData = 'import Qt 4.7\n%s { }' % self.__className__
        component.setData(qmlData, QUrl())

        self._proxy = component.create()
        self._metaObject = self._proxy.metaObject()

        self._scene = parentItem.scene()
        self._scene.addItem(self._proxy)

        t = type(self)
        tDict = t.__dict__
        for key in tDict:
                # connect signals
                if key.startswith('on') and (key in  self.__signals__):
                    signalName = self.__signals__[key]
                    signal = getattr(self._proxy, signalName)
                    signal.connect(getattr(self, key))

                # initialize properties
                elif self._metaObject.indexOfProperty(key) != -1:
                    setattr(self, key, QMLProperty(self._proxy, key, tDict[key]))

                else:
                    try:
                        # istanciate types
                        if issubclass(tDict[key], QMLItem):
                            setattr(self, key, tDict[key](self._proxy))
                    except TypeError:
                        pass

        parent = None

    """
    def _anchors(self):
        if 'anchors' in type(self).__dict__:
            anchor = type(self).__dict__['anchors']
            return anchor.data()
        else:
            return ''
    """

    def __str__(self):
        return type(self).__name__


class Rectangle(QMLItem):
    __className__   = 'Rectangle'

class Image(Rectangle):
    __className__   = 'Image'

class MouseArea(QMLItem):
    __className__   = 'MouseArea'
    __signals__     = {'onClick' : 'clicked'}

