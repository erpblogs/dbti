/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

import { formatDate } from "@web/core/l10n/dates";
import { SkillsX2ManyField, skillsX2ManyField } from "../../../../../hr_skills/static/src/fields/skills_one2many/skills_one2many";
import {CommonSkillsListRenderer} from "../../../../../hr_skills/static/src/views/skills_list_renderer";

export class ValidListRenderer extends CommonSkillsListRenderer {
    get groupBy() {
        return 's_valid_id';
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

ValidListRenderer.template = 'advanced_employee_manager.ValidListRenderer';
ValidListRenderer.rowsTemplate = "advanced_employee_manager.ValidListRenderer.Rows";
ValidListRenderer.recordRowTemplate = "advanced_employee_manager.ValidListRenderer.RecordRow";


export class ValidX2ManyField extends SkillsX2ManyField {
    getWizardTitleName() {
        return _t("Add IDs");
    }
}

ValidX2ManyField.components = {
    ...SkillsX2ManyField.components,
    ListRenderer: ValidListRenderer,
};

export const validX2ManyField = {
    ...skillsX2ManyField,
    component: ValidX2ManyField,
};

registry.category("fields").add("valid_one2many", validX2ManyField);
