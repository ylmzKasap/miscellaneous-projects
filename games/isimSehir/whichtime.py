def tell_time(seconds):
    if seconds < 60:
        return str(round(seconds, 2)) + ' saniye'

    elif seconds < 3600:
        minuteRemainder = seconds // 60
        secondsRemainder = seconds % 60
        return (
                str(minuteRemainder)
                + " dakika "
                + ((str(secondsRemainder)
                    + " saniye") if secondsRemainder > 0 else '')
        )

    elif seconds < 86400:
        hourRemainder = seconds // 3600
        minuteRemainder = (seconds - (hourRemainder * 3600)) // 60
        secondsRemainder = seconds % 60
        return (
                str(hourRemainder)
                + " saat "
                + str(minuteRemainder)
                + " dakika "
                + ((str(secondsRemainder)
                    + " saniye") if secondsRemainder > 0 else '')
        )
    else:
        return f'{str(seconds)} saniye'
