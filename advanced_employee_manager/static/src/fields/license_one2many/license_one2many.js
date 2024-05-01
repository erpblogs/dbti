/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

import { formatDate } from "@web/core/l10n/dates";
import { SkillsX2ManyField, skillsX2ManyField } from "../../../../../hr_skills/static/src/fields/skills_one2many/skills_one2many";
import {CommonSkillsListRenderer} from "../../../../../hr_skills/static/src/views/skills_list_renderer";

export class LicenseListRenderer extends CommonSkillsListRenderer {
    get groupBy() {
        return 's_license';
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

LicenseListRenderer.template = 'advanced_employee_manager.LicenseListRenderer';
LicenseListRenderer.rowsTemplate = "advanced_employee_manager.LicenseListRenderer.Rows";
LicenseListRenderer.recordRowTemplate = "advanced_employee_manager.LicenseListRenderer.RecordRow";


export class LicenseX2ManyField extends SkillsX2ManyField {
    getWizardTitleName() {
        return _t("Add License");
    }
}

LicenseX2ManyField.components = {
    ...SkillsX2ManyField.components,
    ListRenderer: LicenseListRenderer,
};

export const licenseX2ManyField = {
    ...skillsX2ManyField,
    component: LicenseX2ManyField,
};

registry.category("fields").add("license_one2many", licenseX2ManyField);
