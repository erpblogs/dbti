/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

import { formatDate } from "@web/core/l10n/dates";
import { SkillsX2ManyField, skillsX2ManyField } from "../../../../../hr_skills/static/src/fields/skills_one2many/skills_one2many";
import {CommonSkillsListRenderer} from "../../../../../hr_skills/static/src/views/skills_list_renderer";

export class FamilyListRenderer extends CommonSkillsListRenderer {
    get groupBy() {
        return 's_family_member';
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

FamilyListRenderer.template = 'advanced_employee_manager.FamilyListRenderer';
FamilyListRenderer.rowsTemplate = "advanced_employee_manager.FamilyListRenderer.Rows";
FamilyListRenderer.recordRowTemplate = "advanced_employee_manager.FamilyListRenderer.RecordRow";


export class FamilyX2ManyField extends SkillsX2ManyField {
    getWizardTitleName() {
        return _t("Add Family Member");
    }
}

FamilyX2ManyField.components = {
    ...SkillsX2ManyField.components,
    ListRenderer: FamilyListRenderer,
};

export const familyX2ManyField = {
    ...skillsX2ManyField,
    component: FamilyX2ManyField,
};

registry.category("fields").add("family_one2many", familyX2ManyField);
