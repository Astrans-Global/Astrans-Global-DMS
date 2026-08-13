"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.EditItemDto = exports.CreateItemDto = exports.CommandItemDto = void 0;
const class_validator_1 = require("class-validator");
const swagger_1 = require("@nestjs/swagger");
const Validators_1 = require("../../../common/decorators/Validators");
class CommandItemDto {
}
exports.CommandItemDto = CommandItemDto;
__decorate([
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.IsNotEmpty)(),
    (0, class_validator_1.MaxLength)(255),
    (0, swagger_1.ApiProperty)({
        description: 'Item name',
        example: 'Ergonomic Office Chair Model X-2000',
    }),
    __metadata("design:type", String)
], CommandItemDto.prototype, "name", void 0);
__decorate([
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.IsNotEmpty)(),
    (0, class_validator_1.IsIn)(['service', 'non-inventory', 'inventory']),
    (0, swagger_1.ApiProperty)({
        description: 'Item type',
        enum: ['service', 'non-inventory', 'inventory'],
        example: 'inventory',
    }),
    __metadata("design:type", String)
], CommandItemDto.prototype, "type", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.MaxLength)(255),
    (0, swagger_1.ApiProperty)({
        description: 'Item code/SKU',
        required: false,
        example: 'CHAIR-X2000',
    }),
    __metadata("design:type", String)
], CommandItemDto.prototype, "code", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsBoolean)(),
    (0, swagger_1.ApiProperty)({
        description: 'Whether the item can be purchased',
        required: false,
        example: true,
    }),
    __metadata("design:type", Boolean)
], CommandItemDto.prototype, "purchasable", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, Validators_1.ToNumber)(),
    (0, class_validator_1.IsNumber)({ maxDecimalPlaces: 3 }),
    (0, class_validator_1.Min)(0),
    (0, class_validator_1.ValidateIf)((o) => o.purchasable === true),
    (0, swagger_1.ApiProperty)({
        description: 'Cost price of the item',
        required: false,
        minimum: 0,
        example: 299.99,
    }),
    __metadata("design:type", Number)
], CommandItemDto.prototype, "costPrice", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, Validators_1.ToNumber)(),
    (0, class_validator_1.IsInt)(),
    (0, class_validator_1.Min)(0),
    (0, class_validator_1.ValidateIf)((o) => o.purchasable === true),
    (0, swagger_1.ApiProperty)({
        description: 'ID of the cost account',
        required: false,
        minimum: 0,
        example: 1001,
    }),
    __metadata("design:type", Number)
], CommandItemDto.prototype, "costAccountId", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsBoolean)(),
    (0, swagger_1.ApiProperty)({
        description: 'Whether the item can be sold',
        required: false,
        example: true,
    }),
    __metadata("design:type", Boolean)
], CommandItemDto.prototype, "sellable", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, Validators_1.ToNumber)(),
    (0, class_validator_1.IsNumber)({ maxDecimalPlaces: 3 }),
    (0, class_validator_1.Min)(0),
    (0, class_validator_1.ValidateIf)((o) => o.sellable === true),
    (0, swagger_1.ApiProperty)({
        description: 'Selling price of the item',
        required: false,
        minimum: 0,
        example: 399.99,
    }),
    __metadata("design:type", Number)
], CommandItemDto.prototype, "sellPrice", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, Validators_1.ToNumber)(),
    (0, class_validator_1.IsInt)(),
    (0, class_validator_1.Min)(0),
    (0, class_validator_1.ValidateIf)((o) => o.sellable === true),
    (0, swagger_1.ApiProperty)({
        description: 'ID of the sell account',
        required: false,
        minimum: 0,
        example: 2001,
    }),
    __metadata("design:type", Number)
], CommandItemDto.prototype, "sellAccountId", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, Validators_1.ToNumber)(),
    (0, class_validator_1.IsInt)(),
    (0, class_validator_1.Min)(0),
    (0, class_validator_1.ValidateIf)((o) => o.type === 'inventory'),
    (0, swagger_1.ApiProperty)({
        description: 'ID of the inventory account (required for inventory items)',
        required: false,
        minimum: 0,
        example: 3001,
    }),
    __metadata("design:type", Number)
], CommandItemDto.prototype, "inventoryAccountId", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    (0, swagger_1.ApiProperty)({
        description: 'Description shown on sales documents',
        required: false,
        example: 'Premium ergonomic office chair with adjustable height, lumbar support, and breathable mesh back',
    }),
    __metadata("design:type", String)
], CommandItemDto.prototype, "sellDescription", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    (0, swagger_1.ApiProperty)({
        description: 'Description shown on purchase documents',
        required: false,
        example: 'Ergonomic office chair - Model X-2000 with standard features',
    }),
    __metadata("design:type", String)
], CommandItemDto.prototype, "purchaseDescription", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, Validators_1.ToNumber)(),
    (0, class_validator_1.IsInt)(),
    (0, swagger_1.ApiProperty)({
        description: 'ID of the tax rate applied to sales',
        required: false,
        example: 1,
    }),
    __metadata("design:type", Number)
], CommandItemDto.prototype, "sellTaxRateId", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, Validators_1.ToNumber)(),
    (0, class_validator_1.IsInt)(),
    (0, swagger_1.ApiProperty)({
        description: 'ID of the tax rate applied to purchases',
        required: false,
        example: 1,
    }),
    __metadata("design:type", Number)
], CommandItemDto.prototype, "purchaseTaxRateId", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, Validators_1.ToNumber)(),
    (0, class_validator_1.IsInt)(),
    (0, class_validator_1.Min)(0),
    (0, swagger_1.ApiProperty)({
        description: 'ID of the item category',
        required: false,
        minimum: 0,
        example: 5,
    }),
    __metadata("design:type", Number)
], CommandItemDto.prototype, "categoryId", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    (0, swagger_1.ApiProperty)({
        description: 'Additional notes about the item',
        required: false,
        example: 'Available in black, gray, and navy colors. 5-year warranty included.',
    }),
    __metadata("design:type", String)
], CommandItemDto.prototype, "note", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsBoolean)(),
    (0, swagger_1.ApiProperty)({
        description: 'Whether the item is active',
        required: false,
        default: true,
        example: true,
    }),
    __metadata("design:type", Boolean)
], CommandItemDto.prototype, "active", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsArray)(),
    (0, class_validator_1.IsInt)({ each: true }),
    (0, swagger_1.ApiProperty)({
        description: 'IDs of media files associated with the item',
        required: false,
        type: [Number],
        example: [1, 2, 3],
    }),
    __metadata("design:type", Array)
], CommandItemDto.prototype, "mediaIds", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, Validators_1.ToNumber)(),
    (0, class_validator_1.IsNumber)({ maxDecimalPlaces: 4 }),
    (0, class_validator_1.Min)(0),
    __metadata("design:type", Number)
], CommandItemDto.prototype, "packSizeLitres", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.MaxLength)(255),
    __metadata("design:type", String)
], CommandItemDto.prototype, "subcategory", void 0);
class CreateItemDto extends CommandItemDto {
}
exports.CreateItemDto = CreateItemDto;
class EditItemDto extends CommandItemDto {
}
exports.EditItemDto = EditItemDto;
//# sourceMappingURL=Item.dto.js.map