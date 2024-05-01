/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

import { formatDate } from "@web/core/l10n/dates";
import { SkillsX2ManyField, skillsX2ManyField } from "../../../../../hr_skills/static/src/fields/skills_one2many/skills_one2many";
import {CommonSkillsListRenderer} from "../../../../../hr_skills/static/src/views/skills_list_renderer";

export class EducationListRenderer extends CommonSkillsListRenderer {
    get groupBy() {
        return 's_school_name';
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

EducationListRenderer.template = 'advanced_employee_manager.EducationListRenderer';
EducationListRenderer.rowsTemplate = "advanced_employee_manager.EducationListRenderer.Rows";
EducationListRenderer.recordRowTemplate = "advanced_employee_manager.EducationListRenderer.RecordRow";


export class EducationX2ManyField extends SkillsX2ManyField {
    getWizardTitleName() {
        return _t("Create Education");
    }
}

EducationX2ManyField.components = {
    ...SkillsX2ManyField.components,
    ListRenderer: EducationListRenderer,
};

export const educationX2ManyField = {
    ...skillsX2ManyField,
    component: EducationX2ManyField,
};

registry.category("fields").add("education_one2many", educationX2ManyField);
