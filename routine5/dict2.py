# 创建字典的写法
var = {'name': 'gakki', 'age': '23'} # 其实一二是一种方法,但是书上这样写,能有啥办法
d = {}
d['name'] = 'gakki'
d['age'] = 23
# 注意dict是关键字,只是不报错,不能乱用

var3 = dict(name='gakki', age=23) # 关键字创建字典,看起来有点高大上,但是,键必须都是字符串
# 在程序运行时,把key&value逐步建成序列,通常与zip连用
var3 = dict([('name', 'gakki'), ('age', 45)])
# 键和值都相同的字典的初始化
var4 = dict.fromkeys(['name', 'age'], 'xx')

print(var4)

'''
    广度还是 ->精度<-
'''
# zip
# 字典解析 对每一个key - value 构建一个dict
D = {k: v for (k, v) in zip(['a', 'b', 'c'], [1, 2, 3])}
print(D)

D = {x: x**2 for x in [1, 2, 3]}
print(D)

D = {'a'+x: x*4 for x in 'gakki'}
print(D)

D = {c.lower(): c + '!' for c in ['Gakki', 'Gal']}
print(D)

# --------
# t
# 列表解析表达式
#
M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# 把矩阵M中的每一个row中的row[1],放在一个新列表中
col2 = [row[1] for row in M]
col3 = [row[1] for row in M if row[1]%2 == 1]
# 类型只取决于此
col3 = {row[1] for row in M if row[1]%2 == 1}
print(type(col3), col3)
# 简单地对字典的key排序并进行输出
d = {1: 'a', 2: 'b', 3: 'c'}
l = list(d.keys())
l.sort()
for i in l:
    print(i, '=>', d[i])


# -*- coding: utf-8 -*-
import json
import time

from lxml import etree
from openerp.addons.emabc_base.models import base_func as epi

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from openerp.osv import expression
from openerp.osv.orm import setup_modifiers
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

from openerp.exceptions import UserError

MANAGER_ROLE_CODE = ['chief_project_officer_role', 'project_manager_role_', 'project_vice_manager']


class MemberDiff(object):
    def __init__(self, origin_list, new_list):
        self.origin_list, self.new_list = origin_list, new_list
        self.list_is_new = self.added
        self.exist_user = map(lambda x: x[0], origin_list)
        self.new_user = map(lambda x: x[0], new_list)

    def classify(self, _list):
        if _list in self.origin_list:
            return 'unchanged'
        if _list[0] in self.exist_user:
            return 'changed'
        else:
            return 'added'

    def added(self):
        return [x for x in self.new_list if self.classify(x) == 'added']

    def changed(self):
        return [x for x in self.new_list if self.classify(x) == 'changed']

    def removed(self):
        return [x[0] for x in self.origin_list if x[0] not in self.new_user]


class EmabcProject(models.Model):
    _name = 'emabc.project'
    _description = 'Project Information'
    _order = 'project_number'

    _state_selection = {
        'created': 'created',
        'approving': False,
        'approved': 'approved',
        'refused': 'refused'
    }

    state = fields.Selection(selection=[('reconfirm', 'Budget Reconfirm'),
                                        ('new', 'New'),
                                        # ('submitted', 'Budget Submitted'),
                                        ('confirmed', 'Budget Confirmed'),
                                        ('final_confirmed', 'Final Confirmed'),
                                        ('completion_closed', 'Completion Closed'),
                                        ('pre_shutdown', 'Pre-Shutdown'),
                                        ('closed', 'Closed')],
                             string='State', help='State', default='new')
    project_number = fields.Char(string='Project Number', help='Project Number')
    name = fields.Char(string='Name', help='Name', required=True)
    memo = fields.Text(string='Memo', help='Memo')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', help='Partner', ondelete='restrict')
    # project block,its also can be see as child project
    subjob_ids = fields.One2many(comodel_name='emabc.project.subjob',
                                 copy=False,
                                 inverse_name='project_id', string='Subjobs', help='Subjobs')
    project_type_id = fields.Many2one(comodel_name='emabc.base.lookup_value',
                                      domain="[('lookup_type_id.code', '=', 'project_category')]",
                                      string='Project Type', help='Project Type', ondelete='restrict')
    payment_method = fields.Selection(selection=[('milestone', 'Milestone'),
                                                 ('monthly', 'Monthly'),
                                                 ('other', 'Other')],
                                      string='Payment Method', help='Payment Method', default='milestone')
    milestone_ids = fields.One2many(comodel_name='emabc.project.payment.milestone',
                                    inverse_name='project_id',
                                    string='Milestone', help='Milestone')
    # 合同编号
    contract_no = fields.Char(string='Contract No.', help='Contract No.')
    sub_contract_no = fields.Char(string='Sub Contract No.', help='Sub Contract No.')
    # 合同摘要
    payment_cycle = fields.Integer(string='Payment Cycle', help='Payment Cycle', required=True, default=30)
    area_sqm = fields.Float(string='Area (sqm)', help='Area (sqm)')
    project_commencement_date = fields.Date(string='Scheduled Start Date', help='Scheduled Start Date')
    warranty_period = fields.Integer(string='Warranty Period', help='Warranty Period')
    contract_amount = fields.Float(string='Contract Amount (Un-tax)', help='Contract Amount (Un-tax)',
                                   compute='_compute_contract_amount')
    contract_amount_tax=fields.Float(string='Contract Amount Tax', help='Contract Amount Tax')
    project_completion_date=fields.Date(string='Planned Completion Date',help='Planned Completion Date')
    # 合同保修(留)金比例(%)
    warranty_amount_ratio = fields.Integer(string='Contractual warranty (retention) ratio (%)',
                                           help='Contractual warranty (retention) ratio (%)')
    tax_id = fields.Many2one(comodel_name='account.tax', string='Tax/%', help='Tax/%',
                             domain="[('type_tax_use', '=', 'sale'),('price_include','=',True),"
                                    "('company_id','=',company_id)]")
    tax = fields.Integer(string='Tax Number/%', help='Tax Number/%')
    project_substantial_date = fields.Date(string='Planned Substantial Date',help='Planned Substantial Date')
    # 合同保修(留)金额
    warranty_amount=fields.Float(string='Contractual warranty (retention) amount',
                                 help='Contractual warranty (retention) amount')
    project_duration = fields.Integer(string='Project Duration', help='Project Duration')
    duration_type = fields.Selection(selection=[('calendar_days', 'Calendar Days'),
                                                ('working_days', 'Working Days')],
                                     string='Duration Type', help='Duration Type', default='calendar_days')
    project_duration_type = fields.Selection(selection=[('calendar_days', 'Calendar Days'),
                                                ('working_days', 'Working Days')],
                                     string='Duration Type', help='Duration Type', default='calendar_days')
    final_duration_type = fields.Selection(selection=[('calendar_days', 'Calendar Days'),
                                                ('working_days', 'Working Days')],
                                     string='Duration Type', help='Duration Type', default='calendar_days')
    actual_duration_type = fields.Selection(selection=[('calendar_days', 'Calendar Days'),
                                                      ('working_days', 'Working Days')],
                                           string='Duration Type', help='Duration Type', default='calendar_days')

    payment_type = fields.Selection(selection=[('calendar_days', 'Calendar Days'),
                                               ('working_days', 'Working Days')],
                                    string='Payment Type', help='Payment Type', default='calendar_days')
    contract_memo = fields.Text(string='Contract Description', help='Contract Description')
    # 合同保修(留)方式
    quality_assurance_deposit = fields.Selection(selection=[('guarantees','Guarantees'),
                                                            ('cash','Cash')],
                                                 string='Contract warranty (stay) way',
                                                 help='Contract warranty (stay) way',
                                                 default='guarantees')
    province_id = fields.Many2one(comodel_name='emabc.base.lookup_value', string='Province', help='Province')
    province_code = fields.Char(related='province_id.code', readonly=True, string='Province Code', help='Province Code')
    city_id = fields.Many2one(comodel_name='emabc.base.lookup_value', string='City', help='City')
    city_code = fields.Char(related='city_id.code', readonly=True, string='City Code', help='City Code')
    county_id = fields.Many2one(comodel_name='emabc.base.lookup_value', string='Country', help='Country')
    site_addr = fields.Char(string='Site Address', help='Site Address')
    postcode = fields.Char(string='Site Postcode', help='Site Postcode')
    contract_currency_id = fields.Many2one(string='Contract Currency', help='Contract Currency',
                                           comodel_name='res.currency',
                                           default=lambda self: self.env.user.company_id.currency_id or False)
    write_recode_ids = fields.One2many(comodel_name='emabc.project.log', inverse_name='project_id',
                                       string='Time Line', help='Time Line')
    project_member_ids = fields.One2many(comodel_name='emabc.project.member', string='Project Members',
                                         help='Project Members', inverse_name='project_id')
    project_external_member_ids = fields.One2many(comodel_name='emabc.project.external.member',
                                                  string='Project External Members',
                                                  help='Project External Members', inverse_name='project_id')
    project_notice_ids = fields.One2many(comodel_name='emabc.project.notice', string='Project Notice',
                                         help='Project Notice', inverse_name='project_id')
    payment_memo = fields.Text(string='Memo', help='Memo')
    company_id=fields.Many2one(comodel_name='res.company',string='Company',help='Company')
    department_id = fields.Many2one(comodel_name='hr.department',string='Department', help='Department')
    budget_id = fields.Many2one(comodel_name='emabc.project.budget', string='Budget', help='Budget', copy=False)
    budget_state = fields.Selection(related='budget_id.state', string='Budget Status', help='Budget Status', readonly=1)
    have_child = fields.Boolean(compute='_compute_have_child', default=False)
    # 空间类型(Space type)、业主行业(owner industry)
    space_type_id = fields.Many2one(comodel_name='emabc.base.lookup_value',
                                    domain="[('lookup_type_id.code', '=', 'project_space_type')]",
                                    string='Space Type', help='Space Type')
    owner_industry_id = fields.Many2one(comodel_name='emabc.base.lookup_value',
                                        domain="[('lookup_type_id.code', '=', 'project_owner_industry')]",
                                        string='Owner Industry', help='Owner Industry')
    auto_create_child = fields.Boolean(string='Auto Create Child Project', help='Auto Create Child Project',
                                       default=True)
    # 竣工日期Completion Date
    completion_date = fields.Date(string='Completion Date', help='Completion Date')
    # 最终合同金额(含税)Final contract amount (tax included)
    final_contract_amount = fields.Float(string='Final contract amount (tax included)',
                                         help='Final contract amount (tax included)',
                                         compute='_compute_final_contract_amount')
    label_id = fields.Many2one(comodel_name="emabc.base.lookup_value", ondelete='restrict',
                               string="Contractor Label", help="Contractor Label",
                               domain=[('lookup_type_id.code', '=', 'account_move_label_type')])
    access_id = fields.Many2one(comodel_name='project.access', copy=False, string='Access', help='Access')
    # 保修期至
    maintenance_period_to = fields.Date(string='Maintenance Period To', help='Maintenance Period To')
    # 保修备注
    warranty_description = fields.Text(string='Warranty Description', help='Warranty Description')
    # 计划工期(竣工总结)
    schedule_duration = fields.Integer(related='project_duration', string='Project Duration',
                                       help='Project Duration')
    # 计划开工日期(竣工总结)
    project_start_date = fields.Date(related='project_commencement_date', string='Project Start Date',
                                     help='Project Start Date')
    # 计划竣工日期
    project_end_date = fields.Date(related='project_substantial_date', string='Project End Date', help='Project End Date')
    # 实际开工日期
    actual_commencement_date = fields.Date(string='Actual Commencement Date', help='Actual Commencement Date')
    # 实际竣工日期
    actual_substantial_date = fields.Date(string='Actual Substantial Date', help='Actual Substantial Date')
    # 最终计划工期
    final_planning_period = fields.Integer(string='Final Planning Period', help='Final Planning Period')
    # 实际工期
    actual_duration = fields.Integer(string='Actual Duration', help='Actual Duration')
    # 成本&进度备注
    cost_schedule_description = fields.Text(string='Cost And Schedule Description', help='Cost And Schedule Description')
    # 项目预算信息
    budget_ids = fields.One2many(comodel_name='emabc.project.budget', string='Budget Lines', help='Budget Lines',
                                 inverse_name='project_number')
    # 开工预算毛利
    contract_budget_gross_margin = fields.Float(compute='_get_gross_margin', string='Start budget gross margin',
                                                help='Start budget gross margin')
    # 目标毛利
    target_gross_margin = fields.Float(compute='_get_target_gross_margin', string='Target Gross Margin',
                                       help='Target Gross Margin')
    # 开工预算毛利率%
    contract_budget_gross_margin_percentage = fields.Float(compute='_compute_gross_margin',
                                                          string='Start budget gross margin %',
                                                          help='Start budget gross margin %')
    # 目标毛利率%
    completion_goal_gross_margin = fields.Float(compute='_completion_goal_gross_margin', string='Goal Gross Margin %',
                                               help='Goal Gross Margin %')
    # 最终预算毛利
    project_budget_gross_margin = fields.Float(compute='_final_gross_margin',
                                               string='Final Budget Gross Margin',
                                               help='Final budget gross Margin')
    # 最终预算毛利率%
    project_budget_gross_margin_percentage = fields.Float(compute='_final_gross_margin_percentage',
                                                          string='Final Budget Gross Margin %',
                                                          help='Final Budget Gross Margin %')
    # 目标质量
    quality_target = fields.Selection(selection=[('exemplary', 'Exemplary'), ('excellent', 'Excellent'),
                                                 ('standard', 'Standard'), ('bad', 'Bad'), ('poor', 'Poor')],
                                      string='Quality Target', help='Quality Target', default='exemplary')
    # 实际质量
    actual_target = fields.Selection(selection=[('exemplary', 'Exemplary'), ('excellent', 'Excellent'),
                                                ('standard', 'Standard'), ('bad', 'Bad'), ('poor', 'Poor')],
                                     string='Actual Target', help='Actual Target', default='exemplary')
    # 客户满意度
    customer_satisfaction = fields.Selection(selection=[('very_satisfied', 'Very satisfied'),
                                                        ('satisfactory', 'Satisfactory'), ('general', 'General'),
                                                        ('unsatisfactory', 'Unsatisfactory'),
                                                        ('very_dissatisfied', 'Very dissatisfied')],
                                             string='Customer Satisfaction', help='Customer Satisfaction',
                                             default='very_satisfied')
    # 质量&客户满意度备注
    quality_satisfaction_description = fields.Text(string='Quality and customer satisfaction description',
                                                   help='Quality and customer satisfaction description')
    # 总评
    general_comment = fields.Selection(selection=[('very_good', 'Very Good'), ('good', 'Good'),
                                                  ('ordinary', 'Ordinary'), ('not_good', 'Not Good'),
                                                  ('inferior', 'Inferior')], string='General Comment',
                                       help='General Comment', default='very_good')
    # 总评备注
    general_comment_description = fields.Text(string='General Comment Description', help='General Comment Description')
    # 计划复检日期
    planned_re_inspection_date = fields.Date(string='Planned re inspection date', help='Planned re inspection date')
    # 实际复检日期
    actual_re_inspection_date = fields.Date(string='Actual re inspection date', help='Actual re inspection date')
    # 合同达成%
    contract_reaching_percentage = fields.Float(compute='_compute_final_contract_amount',
                                               string='Contract Reaching Percentage %',
                                               help='Contract Reaching Percentage %')
    # 合同含税金额（竣工信息页签）
    completed_contract_amount_tax = fields.Float(string='Contract Amount Tax', help='Contract Amount Tax',
                                                 related='contract_amount_tax')
    # 预算合计 Total budget
    total_budget = fields.Float(string='Total budget', help='Total budget', compute='_compute_total_budget')
    # 附件
    attachment_ids = fields.Many2many(string='Attachment', help='Attachment', comodel_name='ir.attachment',
                                      relation='emabc_project_attachment_rel',
                                      column1='project_id', column2='attachment_id')
    # 项目类别，用于区分正常项目和售前项目
    project_sort = fields.Selection(selection=[('presale', 'Presale'), ('normal', 'Normal')], default='normal',
                                    string="Project Sort",
                                    help="Used for distinguish presale project and normal project")
    back_bid_date = fields.Date(string="Back Bid Date", help="Back Bid Date")
    estimate_start_date = fields.Date(string="Estimate Project Start Date", help="Estimate Project Start Date")
    estimate_end_date = fields.Date(string="Estimate Project End Date", help="Estimate Project End Date")
    pricing_method = fields.Many2one(comodel_name="emabc.base.lookup_value",
                                     domain=[('lookup_type_id.code', '=', 'pricing_method')],
                                     string="Pricing Method", help="Pricing Method")
    pricing_method_remarks = fields.Text(string="Pricing Method Remarks", help="Pricing Method Remarks")
    project_abstract_remarks = fields.Text(string="Project Abstract Remarks", help="Project Abstract Remarks")
    bid_result = fields.Many2one(comodel_name="emabc.base.lookup_value",
                                 domain=[('lookup_type_id.code', '=', 'bid_result')],
                                 string="Bid Result", help="Bid Result")
    # 用户判断中标单位是否可编辑
    bid_result_code = fields.Char(related="bid_result.code", string="Bid Result Code", help="Bid Result Code")
    win_bid_unit = fields.Char(string="Win Bid Unit", help="Win Bid Unit")
    customer_relations = fields.Many2one(comodel_name="emabc.base.lookup_value",
                                         domain=[('lookup_type_id.code', '=', 'customer_relations')],
                                         string="Customer Relations", help="Customer Relations")
    competitor = fields.Text(string="Competitor", help="Competitor")
    net_area = fields.Float(string="Net Area", help="Net Area")
    final_bid_amount = fields.Float(string="Final Bid Amount", help="Final Bid Amount")
    final_bid_gross_margin_percentage = fields.Float(string="Final Bid Gross Margin %", help="Final Bid Gross Margin %")
    final_bid_per_square_meter = fields.Float(string="Final Bid Per Square Meter", help="Final Bid Per Square Meter")
    presale_project_summarize_remarks = fields.Text(string="Presale Project Summarize Remarks",
                                                    help="Presale Project Summarize Remarks")
    # 收入确认方法
    revenue_confirmation_method = fields.Many2one(comodel_name='emabc.revenue.confirmation.method.config.line',
                                                  string='Revenue Confirmation Method',
                                                  help='Revenue Confirmation Method')

    @api.onchange('project_type_id')
    def _onchange_project_type_id(self):
        self.revenue_confirmation_method = False
        if self.project_type_id.id:
            config_id = self.env['emabc.revenue.confirmation.method.config'].search(
                [('project_type', '=', self.project_type_id.id), ('state', '=', 'confirmed')], limit=1)
            for confirmation_method in config_id.confirmation_method_config_line_ids:
                if confirmation_method.revenue_confirmation_method.id == config_id.revenue_confirmation_method.id:
                    self.revenue_confirmation_method = confirmation_method or False

    @api.onchange('bid_result')
    def _onchange_bid_result(self):
        if self.bid_result.code != "outbid":
            self.win_bid_unit = False
            self.customer_relations = False

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        res = super(EmabcProject, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                        toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            if self.env.context.get('is_presale_project_card_action', False):
                res['fields']['state']['selection'][4] = ('completion_closed', _('Completion'))
                for node in doc.xpath("//field[@name='project_type_id']"):
                    node.set('domain', "[('lookup_type_id.code','=','project_category'),('code','=', 'PS')]")
                for node in doc.xpath("//page[@name='page_contract_summarize']"):
                    node.set('string', _('Project Summarize'))
                for node in doc.xpath("//page[@name='page_completion_summary']"):
                    node.set('string', _('Close Summarize'))
            else:
                for node in doc.xpath("//field[@name='project_type_id']"):
                    node.set('domain', "[('lookup_type_id.code','=','project_category'),('code','!=', 'PS')]")
            res['arch'] = etree.tostring(doc)
        return res

    @api.multi
    @api.depends('budget_ids.total_budget')
    def _compute_total_budget(self):
        for rec in self:
            # 找到对应的预算
            project_budget_id = self.env['emabc.project.budget'].search([('project_number', '=', rec.id)], limit=1)
            if project_budget_id:
                rec.total_budget = project_budget_id.total_budget

    @api.multi
    @api.depends('budget_ids.project_budget_gross_margin')
    def _final_gross_margin(self):
        for rec in self:
            # 找到对应的预算
            project_budget_id = self.env['emabc.project.budget'].search([('project_number', '=', rec.id)])
            if project_budget_id:
                rec.project_budget_gross_margin = project_budget_id.mapped('project_budget_gross_margin')[0]

    @api.multi
    @api.depends('budget_ids.project_budget_gross_margin_percentage')
    def _final_gross_margin_percentage(self):
        for rec in self:
            project_budget_id = self.env['emabc.project.budget'].search([('project_number', '=', rec.id)], limit=1)
            if project_budget_id:
                rec.project_budget_gross_margin_percentage = project_budget_id.project_budget_gross_margin_percentage

    @api.multi
    @api.depends('budget_ids.completion_goal_gross_margin')
    def _completion_goal_gross_margin(self):
        for rec in self:
            project_budget_id = self.env['emabc.project.budget'].search([('project_number', '=', rec.id)], limit=1)
            if project_budget_id:
                rec.completion_goal_gross_margin = project_budget_id.completion_goal_gross_margin

    @api.multi
    @api.depends('budget_ids.contract_budget_gross_margin_percentage')
    def _compute_gross_margin(self):
        for rec in self:
            project_budget_id = self.env['emabc.project.budget'].search([('project_number', '=', rec.id)], limit=1)
            if project_budget_id:
                rec.contract_budget_gross_margin_percentage = project_budget_id.contract_budget_gross_margin_percentage

    @api.multi
    @api.depends('budget_ids.target_gross_margin')
    def _get_target_gross_margin(self):
        for rec in self:
            project_budget_id = self.env['emabc.project.budget'].search([('project_number', '=', rec.id)], limit=1)
            if project_budget_id:
                rec.target_gross_margin = project_budget_id.target_gross_margin

    @api.multi
    @api.depends('budget_ids.contract_budget_gross_margin')
    def _get_gross_margin(self):
        for rec in self:
            project_budget_id = self.env['emabc.project.budget'].search([('project_number', '=', rec.id)], limit=1)
            if project_budget_id:
                rec.contract_budget_gross_margin = project_budget_id.contract_budget_gross_margin

    @api.onchange('warranty_amount_ratio')
    def _onchange_warranty_amount_ratio(self):
        self.warranty_amount = 0.00
        if self.warranty_amount_ratio:
            self.warranty_amount = self.contract_amount_tax * self.warranty_amount_ratio/100

    @api.depends('contract_amount_tax')
    def _compute_final_contract_amount(self):
        budget_adjustment_obj = self.env['emabc.project.budget.adjustment']
        for rec in self:
            budget_adjustment_ids = budget_adjustment_obj.search([
                ('state', '=', 'confirmed'),
                ('adjustment_type', '=', 'external'),
                ('project_id', '=', rec.id)
            ])
            amount = 0.0
            for budget_adjustment_id in budget_adjustment_ids:
                amount += budget_adjustment_id.adjusted_contract_amount_tax
            rec.final_contract_amount = amount + rec.contract_amount_tax
            if rec.contract_amount_tax:
                rec.contract_reaching_percentage = (amount + rec.contract_amount_tax) * 100 / rec.contract_amount_tax

    @api.one
    @api.constrains('project_number', 'name')
    def _project_constrains(self):
        if self.search([('id', '!=', self.id), ('company_id', '=', self.company_id.id), ('project_number', '=', self.project_number)], limit=1):
            raise ValidationError(
                _('The project number: {project_number}, the system has the same value, please check and modification.').format(
                    project_number=self.project_number))

        if self.search([('id', '!=', self.id), ('company_id', '=', self.company_id.id), ('name', '=', self.name)], limit=1):
            raise ValidationError(
                _('The project name: {name}, the system has the same value, please check and modification.').format(
                    name=self.name))

    @api.onchange('name')
    def _onchange_name(self):
        for rec in self:
            if rec.name:
                if not rec.subjob_ids:
                    rec.subjob_ids = [[0, 0, {'name': rec.name}]]

    # @api.onchange('name')
    # def _onchange_name(self):
    #     for rec in self.subjob_ids:
    #         if rec.name == self._origin.name:
    #             rec.name = self.name

    @api.onchange('project_number')
    def _onchange_project_number(self):
        for rec in self.subjob_ids:
            if self.project_number:
                rec.code = self.project_number + rec.code[-2:]

    @api.onchange('company_id')
    def _onchange_company(self):
        for rec in self:
            for line in rec.project_member_ids:
                if line.employee_id.company_id.id == rec.company_id.id:
                    pass
                else:
                    line.employee_id = False

    @api.multi
    def action_submit(self):
        for rec in self:
            rec.state = 'submitted'

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    @api.multi
    def action_refuse(self):
        for rec in self:
            rec.state = 'reconfirm'

    @api.multi
    def action_final_confirm(self):
        for rec in self:
            rec.state = 'final_confirmed'

    @api.multi
    def action_completion_closed(self):
        for rec in self:
            rec.state = 'completion_closed'

    @api.multi
    def action_pre_shutdown(self):
        for rec in self:
            rec.suspend_security().state = 'pre_shutdown'

    @api.multi
    def action_closed(self):
        for rec in self:
            rec.suspend_security().state = 'closed'

    @api.multi
    def reset_completion_closed(self):
        for rec in self:
            rec.suspend_security().state = 'completion_closed'

    @api.multi
    def get_contract(self, type='project_manager'):
        rec = self and self[0] or False
        employees = rec and rec.project_member_ids.filtered(lambda x: x.project_role_id.code == type)
        return employees and employees[0].employee_id or False

    @api.multi
    def get_full_attr(self):
        rec = self and self[0] or False
        return rec and ((rec.province_id.name or '') + (rec.city_id.name or "") + (rec.site_addr or "")) or False

    @api.onchange('tax_id')
    def _onchange_tax_id(self):
        for rec in self:
            if rec.tax_id and rec.tax_id.amount:
                rec.tax = int(rec.tax_id.amount)
            else:
                rec.tax = 0

    @api.model
    def create(self, vals):
        if not vals.get('subjob_ids', False) and vals.get('auto_create_child', False):
            res = {}
            res.update({
                'name': (vals['name'] or "")
            })
            vals['subjob_ids'] = [[0, 0, res]]
        context = self.env.context
        if context.get('import_file', False):
            now = fields.Datetime.now()
            lookup_value_obj = self.env['emabc.base.lookup_value']
            active_domain = [('active_from', '<=', now), ('lookup_type_id.active_from', '<=', now),
                             '|', ('active_to', '>=', now), ('active_to', '=', False),
                             '|', ('lookup_type_id.active_to', '>=', now), ('lookup_type_id.active_to', '=', False)]
            if vals.get('label_id', False):
                label_name = lookup_value_obj.browse(vals['label_id']).name
                label_type_code = context.get('label_id', False)
                label_domain = active_domain + [('name', '=', label_name),
                                                ('lookup_type_id.code', '=', label_type_code)]
                label_id = lookup_value_obj.search(label_domain, limit=1)
                vals.update({'label_id': label_id and label_id.id or False})
            if vals.get('project_type_id', False):
                project_type_code = context.get('project_type_id', False)
                project_type_name = lookup_value_obj.browse(vals['project_type_id']).name
                project_type_domain = active_domain + [('name', '=', project_type_name),
                                                       ('lookup_type_id.code', '=', project_type_code)]
                project_type_id = lookup_value_obj.search(project_type_domain, limit=1)
                vals.update({'project_type_id': project_type_id and project_type_id.id or False})
            if vals.get('space_type_id', False):
                space_type_code = context.get('space_type_id', False)
                space_type_name = lookup_value_obj.browse(vals['space_type_id']).name
                space_type_domain = active_domain + [('name', '=', space_type_name),
                                                     ('lookup_type_id.code', '=', space_type_code)]
                space_type_id = lookup_value_obj.search(space_type_domain, limit=1)
                vals.update({'space_type_id': space_type_id and space_type_id.id or False})
            if vals.get('province_id', False):
                province_code = context.get('province_id', False)
                province_type_name = lookup_value_obj.browse(vals['province_id']).name
                province_type_domain = active_domain + [('name', '=', province_type_name),
                                                        ('lookup_type_id.code', '=', province_code)]
                province_type_id = lookup_value_obj.search(province_type_domain, limit=1)
                vals.update({'province_id': province_type_id and province_type_id.id or False})
            if vals.get('city_id', False):
                if not vals.get('province_id'):
                    raise ValidationError(_('The province does not exist!'))
                parent_code = lookup_value_obj.browse(vals['province_id']).code
                city_code = context.get('city_id', False)
                city_type_name = lookup_value_obj.browse(vals['city_id']).name
                city_type_domain = active_domain + [('name', '=', city_type_name),
                                                    ('code', '=like', parent_code + "__"),
                                                    ('lookup_type_id.code', '=', city_code)]
                city_type_id = lookup_value_obj.search(city_type_domain, limit=1)
                if not city_type_id:
                    raise ValidationError(_('City data is incorrect!'))
                vals.update({'city_id': city_type_id and city_type_id.id or False})
            if vals.get('county_id', False):
                if not vals.get('city_id'):
                    raise ValidationError(_('The city does not exist!'))
                county_code = context.get('county_id', False)
                parent_city_code = lookup_value_obj.browse(vals['city_id']).code
                county_type_name = lookup_value_obj.browse(vals['county_id']).name
                city_type_domain = active_domain + [('name', '=', county_type_name),
                                                    ('code', '=like', parent_city_code + "__"),
                                                    ('lookup_type_id.code', '=', county_code)]
                county_type_id = lookup_value_obj.search(city_type_domain, limit=1)
                if not county_type_id:
                    raise ValidationError(_('Country/District data is incorrect!'))
                vals.update({'county_id': county_type_id.id})

        project_id = super(EmabcProject, self).create(vals)
        project_id.sync_access()
        return project_id

    @api.multi
    def unlink(self):
        to_unlink = self.mapped('access_id')
        for rec in self:
            if rec.state != 'new':
                raise ValidationError(_('Non-new status can not be deleted !'))
        if to_unlink:
            to_unlink.with_context(force_unlink=True).unlink()
        return super(EmabcProject, self).unlink()

    @epi.one
    @api.multi
    def _process_member_list(self):
        user_list = []
        for member_line in self.sudo().project_member_ids:
            employee = member_line.employee_id
            user_id = employee.user_id.id
            role_code = member_line.project_role_id.code
            if user_id:
                user_list.append([
                    user_id,
                    member_line.project_role_id.id,
                    employee.id,
                    member_line.project_role_id.name,
                    role_code in MANAGER_ROLE_CODE and 'manager' or 'user'
                ])
        user_list.append([
            self.env.uid,
            False,
            self.env.user.employee_ids[0] and self.env.user.employee_ids[0].id or False,
            False,
            'manager'
        ])
        return user_list

    @api.multi
    def sync_access(self):
        for rec in self:
            if not rec.company_id.project_access_control:
                continue
            new_member = rec._process_member_list()
            access_id = rec.access_id
            if access_id:
                origin_member = access_id.process_access_member()
            else:
                origin_member = []
                access_id = access_id.create({
                    'company_id': rec.company_id.id,
                    'department_id': rec.department_id.id,
                    'project_id': rec.id
                })
                rec.access_id = access_id
            # [用户,角色,员工]
            diff = MemberDiff(origin_member, new_member)
            added = diff.added()
            if added:
                access_id.do_added(added)
            changed = diff.changed()
            if changed:
                access_id.do_changed(changed)
            removed = diff.removed()
            if removed:
                access_id.do_removed(removed)

    @api.onchange('company_id')
    def onchange_contract_currency_default(self):
        self.contract_currency_id = self.company_id.currency_id.id

    @api.onchange('province_id')
    def onchange_province_id(self):
        self.city_id = False

    @api.onchange('city_id')
    def onchange_city_id(self):
        self.county_id = False

    @api.onchange('payment_method')
    def onchange_payment_method_clean(self):
        self.milestone_ids = False
        self.payment_memo = False

    @api.one
    @api.depends('contract_amount_tax', 'tax')
    def _compute_contract_amount(self):
        tax = self.tax_id and float(self.tax_id.amount) / 100 or 0
        self.contract_amount = round(self.contract_amount_tax / (1 + tax), 5)

    @api.one
    @api.onchange('subjob_ids')
    def _compute_have_child(self):
        if self.subjob_ids:
            self.have_child = True
        else:
            self.have_child = False

    @api.model
    def default_get(self, fields_list):
        res = super(EmabcProject, self).default_get(fields_list)
        # 根据context中的is_presale_project_card_action给羡慕卡片默认值
        if self.env.context.get('import_file', False):
            if self.env.context.get('is_presale_project_card_action', False):
                res['project_sort'] = 'presale'
            else:
                res['project_sort'] = 'normal'
        else:
            if self.env.context.get('is_presale_project_card_action', False):
                chief_project_officer_role = self.env.ref('emabc_project.chief_project_officer_role', False)
                marketing_specialist = self.env['emabc.base.lookup_value'].search(
                    [('lookup_type_id.code', '=', 'project_member_role'), ('code', '=', 'marketing_specialist')])
                role_list = []
                line_num = 1
                if chief_project_officer_role:
                    role_list.append([0, 0, {'line_num': line_num, 'line_number': line_num,
                                             'project_role_id': chief_project_officer_role.id}])
                    line_num += 1
                if marketing_specialist:
                    role_list.append([0, 0, {'line_num': line_num, 'line_number': line_num,
                                             'project_role_id': marketing_specialist.id}])
                res['project_member_ids'] = role_list

                res['project_sort'] = 'presale'
                project_type_ps = self.env['emabc.base.lookup_value'].search(
                    [('lookup_type_id.code', '=', 'project_category'), ('code', '=', 'PS')])
                if project_type_ps:
                    res['project_type_id'] = project_type_ps.id
            else:
                chief_project_officer_role = self.env.ref('emabc_project.chief_project_officer_role', False)
                project_manager_role = self.env.ref('emabc_project.project_manager_role', False)
                site_manager_role = self.env.ref('emabc_project.site_manager_role', False)
                project_purchase_role = self.env.ref('emabc_project.project_purchase_role', False)
                project_valuation_role = self.env.ref('emabc_project.project_valuation_role', False)
                role_list = []
                line_num = 1
                if chief_project_officer_role:
                    role_list.append([0, 0, {'line_num': line_num, 'line_number': line_num,
                                             'project_role_id': chief_project_officer_role.id}])
                    line_num += 1
                if project_manager_role:
                    role_list.append([0, 0, {'line_num': line_num, 'line_number': line_num,
                                             'project_role_id': project_manager_role.id}])
                    line_num += 1
                if site_manager_role:
                    role_list.append([0, 0, {'line_num': line_num, 'line_number': line_num,
                                             'project_role_id': site_manager_role.id}])
                    line_num += 1
                if project_purchase_role:
                    role_list.append([0, 0, {'line_num': line_num, 'line_number': line_num,
                                             'project_role_id': project_purchase_role.id}])
                    line_num += 1
                if project_valuation_role:
                    role_list.append([0, 0, {'line_num': line_num, 'line_number': line_num,
                                             'project_role_id': project_valuation_role.id}])
                res['project_member_ids'] = role_list

                res['project_sort'] = 'normal'

        res = self._convert_to_cache(res, validate=False)
        res = self._convert_to_write(res)
        return res

    @api.multi
    def name_get(self):
        result = []
        for pr in self:
            name = pr.name
            code = pr.project_number
            if self._context.get('show_code_only', False):
                result.append((pr.id, code))
            else:
                result.append((pr.id, '[' + code + "]" + name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        pass_domain = []
        access_obj = self.env['project.access']
        if name:
            domain = ['|', ('project_number', 'ilike', name), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&'] + domain
        context = self.env.context
        if not context.get('show_all', False) or context.get('show_all', False) and context[
            'show_all'] != True:
            active_domain = [('state', 'not in', ['pre_shutdown', 'closed'])]
            args += active_domain
            pass_domain = int(str(self._uid)) not in self.get_project_super_users() and [('id', 'in', access_obj.read_acc_ids())] or []
        project = self.search(expression.AND([pass_domain, domain, args]), limit=limit)
        return project.name_get()

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        access_obj = self.env['project.access']
        pass_domain = int(str(self._uid)) not in self.get_project_super_users() and [('id', 'in', access_obj.read_acc_ids())] or []
        domain = expression.AND([pass_domain, domain])
        return super(EmabcProject, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit,
                                                     order=order)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        access_obj = self.env['project.access']
        pass_domain = int(str(self._uid)) not in self.get_project_super_users() and [('id', 'in', access_obj.read_acc_ids())] or []
        domain = expression.AND([pass_domain, domain])
        return super(EmabcProject, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                    orderby=orderby, lazy=lazy)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        access_obj = self.env['project.access']
        pass_domain = int(str(self._uid)) not in self.get_project_super_users() and [('id', 'in', access_obj.read_acc_ids())] or []
        args = expression.AND([pass_domain, args])
        return super(EmabcProject, self).search(args=args, offset=offset, limit=limit, order=order, count=count)

    @api.multi
    def save_current(self):
        pass

    @api.multi
    def write(self, vals):
        for rec in self:
            if len(rec.subjob_ids) == 1:
                if vals.get('name', False):
                    rec.subjob_ids.write({'name': vals['name']})
            # 在项目需重新确认、已确认状态时若已发生请款，则收入确认方法不可更改
            if rec.state in ['reconfirm', 'confirmed'] and vals.get('revenue_confirmation_method', False):
                request_id = self.env['emabc.request.payout'].search([
                    ('project_id', '=', rec.id),
                    ('state', 'in', ['complete', 'part', 'whole', 'cancel'])], limit=1)
                if request_id and rec.revenue_confirmation_method:
                    raise ValidationError(
                        _('There is a correlation payment request of the project, revenue recognition method does not allow changes.'))
        res = super(EmabcProject, self).write(vals)
        self.write_recode_ids.create({
                'project_id': self.id,
                'u_write_id': self.env.user.id,
                'u_write_date': fields.Datetime.now()
            })
        if vals.get('project_member_ids'):
            self.sync_access()
        return res


class EmabcProjectSubjob(models.Model):
    _name = 'emabc.project.subjob'
    _description = 'Project Subjob'

    project_id = fields.Many2one(comodel_name='emabc.project', string='Project', help='Project', ondelete='cascade')
    code = fields.Char(string='Code', help='Code', compute='_compute_code', store=True)
    name = fields.Char(string='Name', help='Name')

    @api.one
    @api.constrains('name')
    def _sub_project_constrains(self):
        if self.search([('id', '!=', self.id), ('project_id', '=', self.project_id.id), ('name', '=', self.name)], limit=1):
            raise ValidationError(
                _('The sub project name: {sub_name}, the system has the same value, please check and modification.').format(
                    sub_name=self.name))

    @api.depends('project_id.project_number')
    def _compute_code(self):
        sequence = 1
        for rec in self:
            if rec.code:
                sequence += 1
            if not rec.code:
                rec.code = str(rec.project_id.project_number) + '0' + str(sequence)
                sequence += 1


class EmabcProjectPaymentMilestone(models.Model):
    _name = 'emabc.project.payment.milestone'
    _description='Project Payment Milestone'

    milestone_point=fields.Char(string="Milestone Point",help="Milestone Point",required=True)
    milestone_datetime=fields.Date(string="Milestone Datetime",help="Milestone Datetime",required=True)
    receipt_ratio = fields.Char(string="Receipt Ratio", help="Receipt Ratio", required=True)
    memo = fields.Char(string="Memo", help="Memo")
    project_id = fields.Many2one(comodel_name="emabc.project",
                                 string="Project", help="Project", ondelete='cascade')
    line_num=fields.Integer(default=0,string="Line Number",help="Line Number")
    line_number=fields.Integer(string="Line Number",help="Line Number",compute='_get_line_number',required=True)

    @api.depends('line_num')
    def _get_line_number(self):
        for line in self:
            line.line_number=line.line_num

    # 获得行号
    @api.model
    def default_get(self,fields_list):
        res=super(EmabcProjectPaymentMilestone,self).default_get(fields_list)
        line_list=self._context.get('milestone_ids',[])
        if line_list:
            line_numbers=[line[2]['line_num'] for line in line_list if
                          line[2] and line[2].has_key('line_num')]
            if line_numbers:
                line_number_value=max(line_numbers) + 1
            else:
                line_number_value=self.browse(max([line[1] for line in line_list]))['line_num'] + 1
        res.update({'line_num': line_number_value if line_list else 1})
        return res


class EmabcProjectLog(models.Model):
    _name = 'emabc.project.log'
    _description = 'Emabc Project Log'
    project_id = fields.Many2one(comodel_name='emabc.project', string='Project', help='Project', ondelete='cascade')
    u_write_id = fields.Many2one(comodel_name='res.users', string='User', help='User')
    u_write_date = fields.Datetime(string='Write Time', help='Write Time')


class EmabcProjectMember(models.Model):
    _name = 'emabc.project.member'
    _description = 'Emabc Project Member'
    line_num = fields.Integer(default=0, string="Line Number", help="Line Number")
    line_number = fields.Integer(string="Line Number", help="Line Number", compute='_get_line_number', required=True)
    project_role_id = fields.Many2one(comodel_name='emabc.base.lookup_value',
                                   domain="[('lookup_type_id.code', '=', 'project_member_role')]",
                                   string='Project Role',
                                   help='Project Role')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', help='Employee')
    memo = fields.Char(string='Memo', help='Memo')
    project_id = fields.Many2one(comodel_name='emabc.project',string='Project',help='Project',ondelete='cascade')
    subjob_id = fields.Many2one(comodel_name='emabc.project.subjob',string='Subjob',help='Subjob')
    work_phone = fields.Char(string='Work Phone', help='Work Phone', related='employee_id.mobile_phone',readonly=True)
    work_email = fields.Char(string='Work Email', help='Work Email', related='employee_id.work_email',readonly=True)
    # project_member_id = fields.Many2one(comodel_name='project.access', related='project_id.access_id' ,string='Project Member')


    @api.depends('line_num')
    def _get_line_number(self):
        for line in self:
            line.line_number = line.line_num

    # 获得行号
    @api.model
    def default_get(self, fields_list):
        res = super(EmabcProjectMember, self).default_get(fields_list)
        line_list = self._context.get('project_member_ids', [])
        if line_list:
            line_numbers = [line[2]['line_num'] for line in line_list if
                            line[2] and line[2].has_key('line_num')]
            if line_numbers:
                line_number_value = max(line_numbers) + 1
            else:
                line_number_value = self.browse(max([line[1] for line in line_list]))['line_num'] + 1
        res.update({'line_num': line_number_value if line_list else 1})
        return res

    # @api.model
    # def create(self, vals):
    #     res = super(EmabcProjectMember, self).create(vals)
    #     project_id = vals.get('project_id', False)
    #     member = {}
    #     if project_id:
    #         access_id = self.env['project.access'].search([('project_id', '=', vals['project_id'])])
    #         if vals.user_id:
    #             access_id.line_ids.write({
    #                 'user_id': vals.employee_id,
    #                 'access_form_type': 'member'
    #             })
    #     return res

      # vals['name'] = vals['analytic_account_plan']
      #   rec = super(EmabcAnalyticAccountPlan, self).create(vals)
      #   if rec.account_ids:
      #       for line in rec.account_ids:
      #           line.write({
      #               'account_plan_id': rec.id,
      #           })
      #   return rec


class EmabcProjectExternalMember(models.Model):
    _name = 'emabc.project.external.member'
    _description = 'Emabc Project External Member'

    project_id = fields.Many2one(comodel_name='emabc.project', string='Project', help='Project',ondelete='cascade')
    line_number = fields.Integer(string="Line Number", help="Line Number")
    project_role_id = fields.Many2one(comodel_name='emabc.base.lookup_value',
                                      domain="[('lookup_type_id.code', '=', 'project_external_member_role')]",
                                      string='Project Role', help='Project Role')
    company = fields.Char(string='Company', help='Company')
    personnel_name = fields.Char(string='Name of Personnel', help='Name of Personnel')
    contact_number = fields.Char(string='Contact Number', help='Contact Number')
    work_email = fields.Char(string='Work E-Mail', help='Work E-Mail')
    memo = fields.Char(string='Memo', help='Memo')


class EmabcProjectNotice(models.Model):
    _name = 'emabc.project.notice'
    _description = 'Project Notice'

    line_num = fields.Integer(default=0, string="Line Number", help="Line Number")
    line_number = fields.Integer(string="Line Number", help="Line Number", compute='_get_line_number', required=True)
    content = fields.Char(string='Content',help='Content')
    due_date = fields.Date(string='Due Date',help='Due Date')
    remind_date = fields.Date(string='Remind Date',help='Remind Date')
    project_id = fields.Many2one(comodel_name='emabc.project', string='Project', help='Project' ,ondelete='cascade')
    # 辅助字段计算提醒次数
    remind_times = fields.Integer(string="Remind Times", help="Remind Times", default=0)
    memo = fields.Char(string='Memo', help='Memo')

    @api.model
    def sent_remind(self):
        lines = self.search([('remind_times', '<', 2), '|', ('due_date', '<=', fields.Datetime.now()),
                             ('remind_date', '<=', fields.Datetime.now())])
        mail_message_obj = self.env['mail.compose.message']
        for line in lines:
            partner_ids = map(lambda x: x.employee_id.user_id.partner_id.id, line.project_id.project_member_ids)
            partner_ids = filter(lambda x: x is not False, partner_ids)
            subject = _("Project Notice:") + "[" + str(
                line.project_id.project_number) + "]" + line.project_id.name
            body = line.content
            if partner_ids:
                vals = {
                    'composition_mode': 'comment',
                    'reply_to': False,
                    'use_active_domain': False,
                    'attachment_ids': [],
                    'template_id': False,
                    'subject': subject,
                    'is_log': False,
                    'mail_server_id': False,
                    'parent_id': False,
                    'body': body,
                    'notify': False,
                    'no_auto_thread': False,
                    'cc_partner_ids': False,
                    'model': 'mail.message',
                    'partner_ids': [[6, False, partner_ids]],
                    'bcc_partner_ids': [],
                    'origin_mail_id': False,
                    'author_id': False,
                    'true_partner_ids': False,
                }
                if line.remind_times<1:
                    line.remind_times = line.remind_times + 1
                    reply_message = mail_message_obj.create(vals)
                    reply_message.send_mail_action()
                if line.remind_times ==1 and time.strptime(line.due_date, DATE_FORMAT) <= \
                        time.strptime(fields.Date.today(), DATE_FORMAT):
                    line.remind_times = line.remind_times + 1
                    reply_message = mail_message_obj.create(vals)
                    reply_message.send_mail_action()

    @api.depends('line_num')
    def _get_line_number(self):
        for line in self:
            line.line_number = line.line_num

    # 获得行号
    @api.model
    def default_get(self, fields_list):
        res = super(EmabcProjectNotice, self).default_get(fields_list)
        line_list = self._context.get('project_notice_ids', [])
        if line_list:
            line_numbers = [line[2]['line_num'] for line in line_list if
                            line[2] and line[2].has_key('line_num')]
            if line_numbers:
                line_number_value = max(line_numbers) + 1
            else:
                line_number_value = self.browse(max([line[1] for line in line_list]))['line_num'] + 1
        res.update({'line_num': line_number_value if line_list else 1})
        return res


class EmabcCostTask(models.Model):
    _inherit = 'emabc.cost.task'

    # 项目
    project_id = fields.Many2one(comodel_name='emabc.project', string='Project Number', help='Project Number')
    project_name = fields.Char(string='Project Name', help='Project Name', related='project_id.name')

    @api.model
    def create(self, vals):
        res = super(EmabcCostTask, self).create(vals)
        project_id = vals.get('project_id', False)
        if res.is_add_task and res.parent_id:
            parent_cost_task = res.browse(vals['parent_id'])
            if project_id:
                exist_add_task = self.search([('project_id', '=', project_id), ('id', '!=', res.id),
                                              ('parent_id', '=', vals['parent_id'])], order='add_seq desc', limit=1)
                add_seq = 1
                if exist_add_task:
                    add_seq = exist_add_task.add_seq +1
                res.add_seq = add_seq
                res.code = parent_cost_task.code + (project_id and str(project_id)) + "A" + str(add_seq).zfill(3)

        return res
    #增补成本任务 project_id,parent_id,name 约束
    @api.constrains('name', 'project_id')
    def constraint_cost_task_name(self):
        for rec in self:
            if self.name and self.is_add_task:
                existed_rec = self.search([('project_id', '=', rec.project_id.id), ('id', '!=', self.id), ('name', '=', self.name),
                                           ('parent_id','=', self.parent_id.id),('is_add_task', '=', True)], limit=1)
                if existed_rec:
                    raise ValidationError(_("The cost task number must be unique in the same project!"))

    #所有成本任务，在删除时增加校验
    @api.multi
    def unlink(self):
        account_analytic_aacount_obj = self.env['account.analytic.account']
        emabc_prohect_budget_line_obj = self.env['emabc.project.budget.line']
        for rec in self:
            #删除的成本任务，是否在项目预算行中存在（是否被使用）
            budget_line_cost_task_exist = emabc_prohect_budget_line_obj.search([
                ('second_cost_task_id', '=', rec.id)
            ],limit =1)
            # 删除的成本任务，是否在分析账户中存在（是否创建了分析账户）
            analytic_account_cost_task_exit = account_analytic_aacount_obj.search([
                '|',('code','=',rec.code),('analytic_acc_code','=',rec.code)
            ],limit =1)
            if analytic_account_cost_task_exit or budget_line_cost_task_exist:
                raise UserError(_('This cost task has been used in the project budget and is not allowed to be deleted. Please check!'))
        return super(EmabcCostTask, self).unlink()

