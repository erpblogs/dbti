/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

import { formatDate } from "@web/core/l10n/dates";
import { SkillsX2ManyField, skillsX2ManyField } from "../../../../../hr_skills/static/src/fields/skills_one2many/skills_one2many";
import {CommonSkillsListRenderer} from "../../../../../hr_skills/static/src/views/skills_list_renderer";

export class ContactNumberListRenderer extends CommonSkillsListRenderer {
    get groupBy() {
        return 's_contact_number';
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

ContactNumberListRenderer.template = 'advanced_employee_manager.ContactNumberListRenderer';
ContactNumberListRenderer.rowsTemplate = "advanced_employee_manager.ContactNumberListRenderer.Rows";
ContactNumberListRenderer.recordRowTemplate = "advanced_employee_manager.ContactNumberListRenderer.RecordRow";


export class ContactNumberX2ManyField extends SkillsX2ManyField {
    getWizardTitleName() {
        return _t("Add Contact Number");
    }
}

ContactNumberX2ManyField.components = {
    ...SkillsX2ManyField.components,
    ListRenderer: ContactNumberListRenderer,
};

export const contactnumberX2ManyField = {
    ...skillsX2ManyField,
    component: ContactNumberX2ManyField,
};

registry.category("fields").add("contactnumber_one2many", contactnumberX2ManyField);
