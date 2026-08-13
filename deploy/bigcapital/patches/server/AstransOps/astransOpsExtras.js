"use strict";

const ITEM_STRIP = ["packSizeLitres", "pack_size_litres", "subcategory"];
const CONTACT_STRIP = [
  "vatTin",
  "vat_tin",
  "areaName",
  "area_name",
  "areaQq",
  "area_qq",
  "creditCategory",
  "credit_category",
];

function knexOf(trxOrModel) {
  if (!trxOrModel) return null;
  if (typeof trxOrModel.raw === "function") return trxOrModel;
  if (typeof trxOrModel.knex === "function") return trxOrModel.knex();
  return null;
}

function firstRow(rawResult) {
  if (!rawResult) return null;
  if (Array.isArray(rawResult) && Array.isArray(rawResult[0])) return rawResult[0][0] || null;
  if (Array.isArray(rawResult)) return rawResult[0] || null;
  return rawResult;
}

function takeItemExtras(dto) {
  const src = dto || {};
  const extras = {
    packSizeLitres: src.packSizeLitres ?? src.pack_size_litres ?? null,
    subcategory: src.subcategory ?? null,
  };
  const rest = { ...src };
  ITEM_STRIP.forEach((k) => {
    delete rest[k];
  });
  return { rest, extras };
}

function takeContactExtras(dto) {
  const src = dto || {};
  const extras = {
    vatTin: src.vatTin ?? src.vat_tin ?? null,
    areaName: src.areaName ?? src.area_name ?? null,
    areaQq: src.areaQq ?? src.area_qq ?? null,
    creditCategory: src.creditCategory ?? src.credit_category ?? "B",
  };
  const rest = { ...src };
  CONTACT_STRIP.forEach((k) => {
    delete rest[k];
  });
  return { rest, extras };
}

async function upsertItemExtras(trxOrModel, itemId, extras) {
  const knex = knexOf(trxOrModel);
  if (!knex || !itemId) return;
  await knex.raw(
    "INSERT INTO ASTRANS_ITEM_EXTRAS (ITEM_ID, PACK_SIZE_LITRES, SUBCATEGORY, UPDATED_AT) VALUES (?, ?, ?, NOW()) ON DUPLICATE KEY UPDATE PACK_SIZE_LITRES=VALUES(PACK_SIZE_LITRES), SUBCATEGORY=VALUES(SUBCATEGORY), UPDATED_AT=NOW()",
    [itemId, extras.packSizeLitres, extras.subcategory],
  );
}

async function loadItemExtras(trxOrModel, itemId) {
  const knex = knexOf(trxOrModel);
  if (!knex || !itemId) return {};
  const row = firstRow(
    await knex.raw(
      "SELECT PACK_SIZE_LITRES AS packSizeLitres, SUBCATEGORY AS subcategory FROM ASTRANS_ITEM_EXTRAS WHERE ITEM_ID = ?",
      [itemId],
    ),
  );
  if (!row) return {};
  return {
    packSizeLitres: row.packSizeLitres ?? row.PACK_SIZE_LITRES ?? null,
    subcategory: row.subcategory ?? row.SUBCATEGORY ?? null,
  };
}

async function upsertContactExtras(trxOrModel, contactId, extras) {
  const knex = knexOf(trxOrModel);
  if (!knex || !contactId) return;
  const cat = extras.creditCategory && /^[A-D]$/i.test(String(extras.creditCategory))
    ? String(extras.creditCategory).toUpperCase()
    : "B";
  await knex.raw(
    "INSERT INTO ASTRANS_CONTACT_EXTRAS (CONTACT_ID, VAT_TIN, AREA_NAME, AREA_QQ, CREDIT_CATEGORY, UPDATED_AT) VALUES (?, ?, ?, ?, ?, NOW()) ON DUPLICATE KEY UPDATE VAT_TIN=VALUES(VAT_TIN), AREA_NAME=VALUES(AREA_NAME), AREA_QQ=VALUES(AREA_QQ), CREDIT_CATEGORY=VALUES(CREDIT_CATEGORY), UPDATED_AT=NOW()",
    [contactId, extras.vatTin, extras.areaName, extras.areaQq, cat],
  );
}

async function loadContactExtras(trxOrModel, contactId) {
  const knex = knexOf(trxOrModel);
  if (!knex || !contactId) return {};
  const row = firstRow(
    await knex.raw(
      "SELECT VAT_TIN AS vatTin, AREA_NAME AS areaName, AREA_QQ AS areaQq, CREDIT_CATEGORY AS creditCategory FROM ASTRANS_CONTACT_EXTRAS WHERE CONTACT_ID = ?",
      [contactId],
    ),
  );
  if (!row) return { creditCategory: "B" };
  return {
    vatTin: row.vatTin ?? row.VAT_TIN ?? null,
    areaName: row.areaName ?? row.AREA_NAME ?? null,
    areaQq: row.areaQq ?? row.AREA_QQ ?? null,
    creditCategory: row.creditCategory ?? row.CREDIT_CATEGORY ?? "B",
  };
}

module.exports = {
  takeItemExtras,
  takeContactExtras,
  upsertItemExtras,
  loadItemExtras,
  upsertContactExtras,
  loadContactExtras,
};
