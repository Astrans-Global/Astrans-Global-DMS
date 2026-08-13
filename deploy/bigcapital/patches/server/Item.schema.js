"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createItemSchema = void 0;
const data_types_1 = require("../../constants/data-types");
const zod_1 = require("zod");
exports.createItemSchema = zod_1.default
    .object({
    name: zod_1.default.string().max(data_types_1.DATATYPES_LENGTH.STRING),
    type: zod_1.default.enum(['service', 'non-inventory', 'inventory']),
    code: zod_1.default.string().max(data_types_1.DATATYPES_LENGTH.STRING).nullable().optional(),
    purchasable: zod_1.default.boolean().optional(),
    cost_price: zod_1.default
        .number()
        .min(0)
        .max(data_types_1.DATATYPES_LENGTH.DECIMAL_13_3)
        .nullable()
        .optional(),
    cost_account_id: zod_1.default
        .number()
        .int()
        .min(0)
        .max(data_types_1.DATATYPES_LENGTH.INT_10)
        .nullable()
        .optional(),
    sellable: zod_1.default.boolean().optional(),
    sell_price: zod_1.default
        .number()
        .min(0)
        .max(data_types_1.DATATYPES_LENGTH.DECIMAL_13_3)
        .nullable()
        .optional(),
    sell_account_id: zod_1.default
        .number()
        .int()
        .min(0)
        .max(data_types_1.DATATYPES_LENGTH.INT_10)
        .nullable()
        .optional(),
    inventory_account_id: zod_1.default
        .number()
        .int()
        .min(0)
        .max(data_types_1.DATATYPES_LENGTH.INT_10)
        .nullable()
        .optional(),
    sell_description: zod_1.default
        .string()
        .max(data_types_1.DATATYPES_LENGTH.TEXT)
        .nullable()
        .optional(),
    purchase_description: zod_1.default
        .string()
        .max(data_types_1.DATATYPES_LENGTH.TEXT)
        .nullable()
        .optional(),
    sell_tax_rate_id: zod_1.default.number().int().nullable().optional(),
    purchase_tax_rate_id: zod_1.default.number().int().nullable().optional(),
    category_id: zod_1.default
        .number()
        .int()
        .min(0)
        .max(data_types_1.DATATYPES_LENGTH.INT_10)
        .nullable()
        .optional(),
    note: zod_1.default.string().max(data_types_1.DATATYPES_LENGTH.TEXT).optional(),
    active: zod_1.default.boolean().optional(),
    media_ids: zod_1.default.array(zod_1.default.number().int()).optional(),
    packSizeLitres: zod_1.default.number().min(0).nullable().optional(),
    pack_size_litres: zod_1.default.number().min(0).nullable().optional(),
    subcategory: zod_1.default.string().max(255).nullable().optional(),
})
    .refine((data) => {
    if (data.purchasable) {
        return (data.cost_price !== undefined && data.cost_account_id !== undefined);
    }
    return true;
}, {
    message: 'Cost price and cost account ID are required when item is purchasable',
    path: ['cost_price', 'cost_account_id'],
})
    .refine((data) => {
    if (data.sellable) {
        return (data.sell_price !== undefined && data.sell_account_id !== undefined);
    }
    return true;
}, {
    message: 'Sell price and sell account ID are required when item is sellable',
    path: ['sell_price', 'sell_account_id'],
})
    .refine((data) => {
    if (data.type === 'inventory') {
        return data.inventory_account_id !== undefined;
    }
    return true;
}, {
    message: 'Inventory account ID is required for inventory items',
    path: ['inventory_account_id'],
});
//# sourceMappingURL=Item.schema.js.map