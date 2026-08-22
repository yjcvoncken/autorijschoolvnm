from django.db import models


class SiteSettings(models.Model):
    hero_title = models.CharField("hoofdtitel", max_length=160, default="Samen op weg naar jouw rijbewijs!")
    hero_text = models.TextField("introductietekst", default="Persoonlijke rijlessen in Nijmegen, met geduld, vertrouwen en begeleiding die écht bij jou past.")
    about_title = models.CharField("titel over ons", max_length=160, default="Rijles met aandacht voor jou")
    about_text = models.TextField("tekst over ons", default="Bij Autorijschool VNM staat jouw ontwikkeling centraal. Je krijgt les in een rustige, prettige sfeer en werkt stap voor stap aan veilig en zelfverzekerd rijgedrag.")
    instructor = models.CharField("naam instructeur", max_length=100, default="Yasser")
    success_rate = models.PositiveSmallIntegerField("slagingspercentage", default=76)
    phone = models.CharField("telefoonnummer", max_length=30, default="06 - 28 868 238")
    email = models.EmailField("e-mailadres", default="autorijschoolvnm1971@hotmail.com")
    notification_email = models.EmailField(
        "ontvangstadres formulieren",
        blank=True,
        help_text="Bijvoorbeeld je Gmail-adres. Leeg laten om het openbare e-mailadres te gebruiken.",
    )
    address = models.CharField("adres", max_length=200, default="Voorstenkamp 13-27, 6545 EP Nijmegen")
    city = models.CharField("plaats", max_length=100, default="Nijmegen")
    whatsapp = models.CharField("WhatsApp-nummer", max_length=30, default="31628868238", help_text="Alleen cijfers, inclusief landcode.")
    facebook_url = models.URLField(
        "Facebook-link",
        blank=True,
        default="https://www.facebook.com/people/Autorijschool-Vnm/100078653213544/",
    )
    instagram_url = models.URLField(
        "Instagram-link",
        blank=True,
        default="https://www.instagram.com/autorijschoolvnm/",
    )

    class Meta:
        verbose_name = "website-instelling"
        verbose_name_plural = "website-instellingen"

    def __str__(self):
        return "Website-instellingen"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class ContactInformation(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "contactgegeven"
        verbose_name_plural = "contactgegevens"


class Package(models.Model):
    name = models.CharField("naam", max_length=100)
    price = models.CharField("prijs", max_length=40, help_text="Bijvoorbeeld € 699 of Op aanvraag")
    label = models.CharField("label", max_length=50, blank=True)
    description = models.TextField("omschrijving")
    features = models.TextField("kenmerken", help_text="Eén kenmerk per regel")
    featured = models.BooleanField("uitgelicht", default=False)
    order = models.PositiveSmallIntegerField("volgorde", default=0)
    active = models.BooleanField("zichtbaar", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "lespakket"
        verbose_name_plural = "lespakketten"

    def __str__(self):
        return self.name

    @property
    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]


class GalleryImage(models.Model):
    title = models.CharField("titel", max_length=120, blank=True)
    image = models.ImageField("foto", upload_to="gallery/")
    alt_text = models.CharField("alternatieve tekst", max_length=160, blank=True)
    order = models.PositiveSmallIntegerField("volgorde", default=0)
    active = models.BooleanField("zichtbaar", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "galerijfoto"
        verbose_name_plural = "galerijfoto's"

    def __str__(self):
        return self.title or f"Galerijfoto {self.pk}"


class ContactRequest(models.Model):
    SUBJECTS = [
        ("proefles", "Ik wil een proefles plannen"),
        ("pakketten", "Ik heb een vraag over pakketten"),
        ("informatie", "Ik wil meer informatie"),
    ]
    name = models.CharField("naam", max_length=120)
    phone = models.CharField("telefoonnummer", max_length=30)
    email = models.EmailField("e-mailadres")
    package = models.ForeignKey(
        Package,
        verbose_name="gekozen pakket",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_requests",
    )
    subject = models.CharField("onderwerp", max_length=30, choices=SUBJECTS, default="proefles")
    message = models.TextField("bericht", blank=True)
    handled = models.BooleanField("afgehandeld", default=False)
    created_at = models.DateTimeField("ontvangen op", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "contactaanvraag"
        verbose_name_plural = "contactaanvragen"

    def __str__(self):
        return f"{self.name} – {self.get_subject_display()}"
