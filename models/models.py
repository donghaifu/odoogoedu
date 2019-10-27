# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'odoogoedu.course'
    _description = "课程记录"
    name = fields.Char(string="课程名", required=True)
    description = fields.Text(string="课程描述")
    #多个课程，指向一个负责人
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="负责人", index=True)
    #一个课程，对应多个课时，与课时模型中的course_id对应
    session_ids = fields.One2many('odoogoedu.session', 'course_id', string="课时")


class Session(models.Model):
    _name = 'odoogoedu.session'
    _description = "课时"

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="时长（天）")
    seats = fields.Integer(string="座位数")
    #多个课时，指向一个指导老师
    #使用domain过滤出只是老师的partner记录
    #instructor_id = fields.Many2one('res.partner',string="老师",domain=[('instructor','=',True)])
    #instructor_id = fields.Many2one('res.partner',string="老师")
    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])
    #多个课时，指向一个课程
    course_id = fields.Many2one('odoogoedu.course', ondelete='cascade', string="课程", required=True)
    #课时和学生是多对多的关系
    attendee_ids = fields.Many2many('res.partner', string="学生")


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