# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import random

class Course(models.Model):
    _name = 'odoogoedu.course'
    _description = "课程记录"
    name = fields.Char(string="课程名", required=True)
    description = fields.Text(string="课程描述")
    #多个课程，指向一个负责人
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="负责人", index=True)
    #一个课程，对应多个课时，与课时模型中的course_id对应
    session_ids = fields.One2many('odoogoedu.session', 'course_id', string="课时")

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "课程名与课程描述不能相同"),

        ('name_unique',
         'UNIQUE(name)',
         "课程名不能重复"),
    ]


    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"%{}的副本".format(self.name))])
        if not copied_count:
            new_name = u"{}的副本".format(self.name)
        else:
            new_name = u"{} ({})的副本".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)



class Session(models.Model):
    _name = 'odoogoedu.session'
    _description = "课时"

    name = fields.Char(required=True)

    #默认值
    @api.model
    def _get_current_date(self):
        """ :return current date """
        return fields.Date.today()

    #start_date = fields.Date(required=True, default=lambda self: self._get_current_date())
    start_date = fields.Date(default=lambda self: self._get_current_date())

    active = fields.Boolean(default=True)

    def get_user(self):
        print(self)
        print(self.env)
        print(self.env.cr)
        print(self.env.uid)
        print(self.env.user)
        print(self.env.context)
        print(self.env.ref)
        print(self.env['res.users'])
        return self.env.uid
    #user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', default=get_user)

    duration = fields.Float(digits=(6, 2), help="时长（天）",default=1)

    #Many2one:多个课时，指向一个指导老师
    #使用domain过滤出只是老师的partner记录
    #instructor_id = fields.Many2one('res.partner',string="老师",domain=[('instructor','=',True)])
    #instructor_id = fields.Many2one('res.partner',string="老师")
    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])
    #多个课时，指向一个课程
    course_id = fields.Many2one('odoogoedu.course', ondelete='cascade', string="课程", required=True)

    #Many2Many:课时和学生是多对多的关系
    attendee_ids = fields.Many2many('res.partner', string="学生")

    #依赖
    seats = fields.Integer(string="座位数")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
            #r.test_name = str(random.randint(1, 1e6))
            #r.duration = str(random.randint(1, 1e6))

    #onchange方法
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        #self.test_name = str(random.randint(1, 1e6))
        #self.duration = str(random.randint(1, 1e6))
        #根据seats和attendee_ids改变，验证用户输入座位数不能为负数
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        #座位数不能小于现有出席人数
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }

    #计算字段
    test_name = fields.Char(compute='_compute_name')
    @api.multi
    #@api.depends("seats")
    def _compute_name(self):
        print(self)                   #self是一个record集合(recordset),可以for循环出里面的单个记录（record），recordset还支持+号操作
        for record in self:
            print(record)             #代表单个记录
            record.test_name = str(random.randint(1, 1e6))
            print(record.test_name)   #单个记录可以用 . 来访问字段

    #python代码级别模型约束
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("老师不出现在学生列表中")

#继承
class Extension0(models.Model):
    _name = 'extension.0'
    name = fields.Char(default="A")


class Extension1(models.Model):
    _name = 'extension.0'  # 相同可以省略不写
    _inherit = 'extension.0'
    description = fields.Char(default="Extended")


class Inheritance0(models.Model):
    _name = 'inheritance.0'
    name = fields.Char()

    def call(self):
        return self.check("model 0")

    def check(self, s):
        return "This is {} record {}".format(s, self.name)

class Inheritance1(models.Model):
    _name = 'inheritance.1'
    _inherit = 'inheritance.0'

    def call(self):
        return self.check("model 1")


class Child0(models.Model):
    _name = 'delegation.child0'
    field_0 = fields.Integer()

class Child1(models.Model):
    _name = 'delegation.child1'
    field_1 = fields.Integer()

class Delegating(models.Model):
    _name = 'delegation.parent'
    _inherits = {
        'delegation.child0': 'child0_id',
        'delegation.child1': 'child1_id',
    }
    child0_id = fields.Many2one('delegation.child0', required=True, ondelete='cascade')
    child1_id = fields.Many2one('delegation.child1', required=True, ondelete='cascade')



# class odoogoedu(models.Model):
#     _name = 'odoogoedu.odoogoedu'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100