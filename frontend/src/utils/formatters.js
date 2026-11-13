const LOCALE = "es-CO";
const MONEY_DECIMALS = 2;
const INDEX_DECIMALS = 2;
const NOT_AVAILABLE = "N/D";

const moneyFormat = new Intl.NumberFormat(LOCALE, {
  minimumFractionDigits: MONEY_DECIMALS,
  maximumFractionDigits: MONEY_DECIMALS,
});
const indexFormat = new Intl.NumberFormat(LOCALE, {
  minimumFractionDigits: INDEX_DECIMALS,
  maximumFractionDigits: INDEX_DECIMALS,
});

export const formatMoney = (value) => (value == null ? NOT_AVAILABLE : moneyFormat.format(value));
export const formatIndex = (value) => (value == null ? NOT_AVAILABLE : indexFormat.format(value));
export const formatPercent = (value) => `${value}%`;
