export function stepSequence(eta, count = 8) {
  let x = 0
  return Array.from({ length: count + 1 }, (_, k) => {
    const point = { k, x, error: Math.abs(x - 2), value: (x - 2) ** 2 }
    x -= eta * 2 * (x - 2)
    return point
  })
}
