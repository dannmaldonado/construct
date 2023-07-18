from django.shortcuts import render, redirect
from .models import Categoria, Produto, Imagem
from django.http import HttpResponse
from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.urls import reverse
from django.contrib import messages


def add_produto(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        produtos = Produto.objects.all()
        return render(request, 'add_produto.html', {'categorias': categorias, 'produtos': produtos})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        quantidade = request.POST.get('quantidade')
        preco_compra = request.POST.get('preco_compra')
        preco_venda = request.POST.get('preco_venda')

        produto = Produto(nome=nome,
                          categoria_id=categoria,
                          quantidade=quantidade,
                          preco_compra=preco_compra,
                          preco_venda=preco_venda)

        produto.save()

        # Jeito de fazer sem tratamento das imagens
        # for f in request.FILES.getlist('imagens'):
        #     img = Imagem(imagem=f, produto=produto)
        #     img.save()

        for f in request.FILES.getlist('imagens'):
            name = f'{date.today()}-{produto.id}.jpg'

            img = Image.open(f)
            img = img.convert('RGB')  # convert o padrão de cor das imagens
            # redimensiona a imagem para o tamanho definido
            img = img.resize((800, 600))
            draw = ImageDraw.Draw(img)
            # coloca marca dagua na imagem, sendo: posição, texto, data se quiser, e cor em rgb
            draw.text((20, 580), f"CONSTRUCT {date.today()}", (255, 255, 255))
            output = BytesIO()  # converte a imagem em bytes
            # salva a imagem no caminho (output), com o formato e qualidade definidos
            img.save(output, format="JPEG", quality=100)
            output.seek(0)
            img_final = InMemoryUploadedFile(
                output, 'ImageField', name, 'image/jpeg', sys.getsizeof(output), None)  # converte os bytes do output em imagem novamente

            img_dj = Imagem(imagem=img_final, produto=produto)
            img_dj.save()
        messages.add_message(request, messages.SUCCESS,
                             'Produto cadastrato com sucesso')
        return redirect(reverse('add_produto'))
