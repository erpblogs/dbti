/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

import { formatDate } from "@web/core/l10n/dates";
import { SkillsX2ManyField, skillsX2ManyField } from "../../../../../hr_skills/static/src/fields/skills_one2many/skills_one2many";
import {CommonSkillsListRenderer} from "../../../../../hr_skills/static/src/views/skills_list_renderer";

export class CompensationBenefitListRenderer extends CommonSkillsListRenderer {
    get groupBy() {
        return 's_transaction_type';
    }

    get colspan() {
        if (this.props.activeActions) {
            return 3;
        }
        return 2;
    }

    formatDate(date) {
        return formatDate(date);
    }

    setDefaultColumnWidths() {
    }
}

CompensationBenefitListRenderer.template = 'advanced_employee_manager.CompensationBenefitListRenderer';
CompensationBenefitListRenderer.rowsTemplate = "advanced_employee_manager.CompensationBenefitListRenderer.Rows";
CompensationBenefitListRenderer.recordRowTemplate = "advanced_employee_manager.CompensationBenefitListRenderer.RecordRow";


export class CompensationBenefitX2ManyField extends SkillsX2ManyField {
    getWizardTitleName() {
        return _t("ADD Compensation And Benefit");
    }
}

CompensationBenefitX2ManyField.components = {
    ...SkillsX2ManyField.components,
    ListRenderer: CompensationBenefitListRenderer,
};

export const compensationbenefitX2ManyField = {
    ...skillsX2ManyField,
    component: CompensationBenefitX2ManyField,
};

registry.category("fields").add("compensationbenefit_one2many", compensationbenefitX2ManyField);
