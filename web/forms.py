# coding: utf-8

from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, SubmitField, DecimalField
from wtforms.validators import Required, Regexp, NumberRange, ValidationError

def validate_prime(form, field):
    def gcd(a, b):
        while b:
            a, b = b, a%b
        return a
        
    if gcd(int(field.data), 26) != 1:
        raise ValidationError(u"k2需与26互质") 

class ClassicCryptForm(Form):
    text = TextAreaField(u"请输入原文(仅限英文)")
    cipher = TextAreaField(u"请输入密文(仅限英文)")
    key1 = StringField(u"请输入密钥k1", validators=[Required(),
                            Regexp(r"^[0123456789]+$", message=u"请输入整数")])
    key2 = StringField(u"请输入密钥k2", validators=[Required(),
                            Regexp(r"^[0123456789]+$", message=u"请输入整数"),
                            validate_prime])
    encrypt = SubmitField(u"加密")
    decrypt = SubmitField(u"解密")
    stat = SubmitField(u"统计")

class DESCryptForm(Form):
    text = TextAreaField(u"请输入原文")
    key = StringField(u"请输入密钥 (14位16进制数字, 如11223344aabbcc)",
                         validators=[Required(), 
                         Regexp(r"^[0-9a-fA-F]{14}$", message=u"请输入14位16进制数字")])
    encrypt = SubmitField(u"加密 ↓")
    decrypt = SubmitField(u"解密 ↑") 
    cipher = TextAreaField(u"请输入密文")

class RSACryptForm(Form):
    text = TextAreaField(u"请输入原文", 
                    validators=[Regexp(r"^[A-Za-z ]*$", message=u"仅支持字母与空格")],
                    default=u"I LOVE YOU")
    encrypt = SubmitField(u"加密 ↓")
    decrypt = SubmitField(u"解密 ↑") 
    cipher = TextAreaField(u"请输入密文")

class LFSRCryptForm(Form):
    text = TextAreaField(u"请输入原文", 
                    validators=[])
    key = DecimalField(u"密钥", validators=[Required(), NumberRange(1, 31, u"密钥应为1-31的整数")])
    encrypt = SubmitField(u"加密 ↓")
    decrypt = SubmitField(u"解密 ↑") 
    cipher = TextAreaField(u"请输入密文")

class DSASignForm(Form):
    text = TextAreaField(u"请输入需签名/认证的信息", validators=[Required()])
    sha = StringField(u"信息SHA散列")
    signature = StringField(u"DSA签名", validators=[])
    sign = SubmitField(u"签名")
    verify = SubmitField(u"验证")

